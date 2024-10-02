import logging
import os
from typing import Collection, List, Mapping, Optional

import mlflow
import pandas as pd

from databricks.rag_eval import constants, schemas
from databricks.rag_eval.evaluation import entities, traces
from databricks.rag_eval.judges import builtin_judge
from databricks.rag_eval.utils import error_utils

_logger = logging.getLogger(__name__)


def compute_eval_metrics(
    assessment_log: entities.AssessmentLog,
) -> entities.EvalResult:
    """
    Compute the per-eval-item metrics and produce the eval result.

    The aggregation is performed on the per-eval-item granularity – for each eval-item in the input eval dataset,
    this function produces an EvalResult.
    """
    eval_item = assessment_log.eval_item
    trace_token_count = traces.compute_total_token_count(eval_item.trace)

    overall_assessment = _compute_overall_assessment(assessment_log.assessment_results)

    if (
        os.environ.get(constants.AGENT_EVAL_SHOW_RCA_RATIONALE) != "true"
        and overall_assessment is not None
    ):
        overall_assessment.rationale = None

    return entities.EvalResult(
        eval_item=eval_item,
        assessment_results=assessment_log.assessment_results,
        overall_assessment=overall_assessment,
        total_input_token_count=trace_token_count.input_token_count,
        total_output_token_count=trace_token_count.output_token_count,
        total_token_count=trace_token_count.total_token_count,
        exact_match=_compute_exact_match(eval_item),
        latency_seconds=_compute_latency_seconds(eval_item),
        ground_truth_retrieval_metrics=_compute_ground_truth_retrieval_metrics(
            eval_item
        ),
        llm_judged_retrieval_metrics=_compute_llm_judged_retrieval_metrics(
            assessment_log.assessment_results
        ),
        ground_truth_document_ratings=_compute_ground_truth_document_ratings(eval_item),
    )


# ================ Latency ================
def _compute_latency_seconds(eval_item: entities.EvalItem) -> Optional[float]:
    """Compute the latency (in fractional seconds to a microsecond granularity) from the trace information."""
    if (
        eval_item.trace is None
        or eval_item.trace.info is None
        or eval_item.trace.info.execution_time_ms is None
    ):
        return None
    else:
        return eval_item.trace.info.execution_time_ms / 1000.0


# ================ Exact Match ================
def _compute_exact_match(
    eval_item: entities.EvalItem,
) -> Optional[bool]:
    """Compute the exact match. The answer is considered an exact match if it is equal to the ground truth answer."""
    if eval_item.answer is None or eval_item.ground_truth_answer is None:
        return None
    return eval_item.answer.strip() == eval_item.ground_truth_answer.strip()


# ================ Ground Truth Retrieval Metrics ================
def _compute_ground_truth_retrieval_metrics(
    eval_item: entities.EvalItem,
) -> Mapping[str, float]:
    """
    Compute the ground truth retrieval metrics.

    The ground truth retrieval metrics include: precision, recall, etc.

    The metrics is calculated based on the doc_uri of retrieval context and ground truth retrieval context
    in the eval item.

    The method outputs the following metrics:
    - The recall for the whole context (K = length of retrieval)
    """
    if not eval_item.retrieval_context or not eval_item.ground_truth_retrieval_context:
        return {}
    retrieved_docs = eval_item.retrieval_context.get_doc_uris()
    ground_truth_docs = eval_item.ground_truth_retrieval_context.get_doc_uris()
    if not retrieved_docs or not ground_truth_docs:
        return {}

    results = {}
    k = len(retrieved_docs)
    for metric_name in constants.GROUND_TRUTH_RETRIEVAL_METRIC_NAMES:
        mlflow_eval_metric = getattr(mlflow.metrics, f"{metric_name}_at_k")(k)

        eval_fn = mlflow_eval_metric.eval_fn
        try:
            metric_value = eval_fn(
                pd.Series([retrieved_docs]), pd.Series([ground_truth_docs])
            )
            score = metric_value.scores[0]
            results[f"{schemas.GROUND_TRUTH_DOCUMENT_PREFIX}{metric_name}"] = score
        except Exception as e:
            full_metric_name = (
                schemas.GROUND_TRUTH_RETRIEVAL_METRIC_COL_PREFIX
                + schemas.GROUND_TRUTH_DOCUMENT_PREFIX
                + metric_name
            )
            _logger.debug(
                f"Error in computing {full_metric_name} for eval_item {eval_item}: {e}"
            )

    return results


# ================ Ground Truth Document Ratings ================
def _compute_ground_truth_document_ratings(
    eval_item: entities.EvalItem,
) -> Optional[List[entities.CategoricalRating]]:
    """
    Compute the ground truth retrieved document ratings.

    The ratings are calculated based on the doc_uri of retrieval context and ground truth retrieval context.
    For each document in the retrieval context, we rate it Yes if it is in the ground truth retrieval context,
    and No otherwise.

    Return None if the retrieval context or ground truth retrieval context is None.
    """
    if not eval_item.retrieval_context or not eval_item.ground_truth_retrieval_context:
        return None
    retrieved_docs = eval_item.retrieval_context.get_doc_uris()
    ground_truth_docs = eval_item.ground_truth_retrieval_context.get_doc_uris()
    if not retrieved_docs or not ground_truth_docs:
        return None

    return [
        (
            (
                entities.CategoricalRating.YES
                if retrieved_doc in ground_truth_docs
                else entities.CategoricalRating.NO
            )
            if retrieved_doc is not None
            else None
        )
        for retrieved_doc in retrieved_docs
    ]


# ================ LLM Judged Retrieval Metrics ================
def _compute_llm_judged_retrieval_metrics(
    assessment_results: Collection[entities.AssessmentResult],
) -> Mapping[str, float]:
    """
    Compute the LLM-judged precision metrics using the results of the retrieval assessment.

    We use the positional_rating of the retrieval assessment results to compute the precision at k metrics.
    """
    results = {}
    for assessment_result in assessment_results:
        if not isinstance(assessment_result, entities.PerChunkAssessmentResult):
            continue
        ratings = [
            rating
            for _, rating in assessment_result.positional_rating.items()
            if rating.categorical_value is not None
        ]
        if not ratings:
            continue
        precision = sum(
            r.categorical_value == entities.CategoricalRating.YES for r in ratings
        ) / len(ratings)
        results[f"{assessment_result.assessment_name}/precision"] = precision
    return results


# ================ Overall assessment ================
def _compute_overall_assessment(
    assessment_results: Collection[entities.AssessmentResult],
) -> Optional[entities.Rating]:
    """
    Compute the overall assessment based on the individual assessment results and applying our RCA logic.

    The categorical rating contains a high-level tag describing quality issues. If our logic does
    not recognize the set of judges, we return `YES` or `NO` based on a logical AND of all judges.
    Note that all errors are ignored in the logical AND.

    The rationale contains the root cause analysis (RCA) and potential fixes based on the assessment
    results. If a required judge is missing, the RCA will be empty. If all judges are passing, the
    RCA will be empty.
    """
    # Filter out errored per-request assessments or fully errored per-chunk assessments out of RCA
    filtered_assessment_results = [
        assessment_result
        for assessment_result in assessment_results
        if (
            isinstance(assessment_result, entities.PerRequestAssessmentResult)
            and assessment_result.rating.error_code is None
        )
        or (
            isinstance(assessment_result, entities.PerChunkAssessmentResult)
            and any(
                rating.error_code is None
                for rating in assessment_result.positional_rating.values()
            )
        )
    ]
    if not len(filtered_assessment_results):
        return None

    assessment_results_mapping = {
        assessment_result.assessment_name: assessment_result
        for assessment_result in filtered_assessment_results
    }

    all_assessments_positive = all(
        [
            _assessment_is_yes(assessment_result)
            for assessment_result in filtered_assessment_results
        ]
    )

    default_overall_rating = entities.Rating.value(
        categorical_value=(
            entities.CategoricalRating.YES
            if all_assessments_positive
            else entities.CategoricalRating.NO
        ),
        rationale=(
            None if all_assessments_positive else constants.DEFAULT_FAILED_SUGGESTION
        ),
    )

    context_sufficiency_assessment = assessment_results_mapping.get(
        builtin_judge.CONTEXT_SUFFICIENCY.assessment_name
    )
    chunk_relevance_assessment = assessment_results_mapping.get(
        builtin_judge.CHUNK_RELEVANCE.assessment_name
    )
    if context_sufficiency_assessment is None and chunk_relevance_assessment is None:
        # Return default rating early if RCA does not exist
        return default_overall_rating
    elif _assessment_is_no(context_sufficiency_assessment):
        return entities.Rating.value(
            categorical_value=entities.CategoricalRating.NO,
            rationale=constants.CONTEXT_SUFFICIENCY_FAILED_SUGGESTION,
        )
    elif _assessment_is_no(chunk_relevance_assessment):
        return entities.Rating.value(
            categorical_value=entities.CategoricalRating.NO,
            rationale=constants.CHUNK_RELEVANCE_FAILED_SUGGESTION,
        )

    groundedness_assessment = assessment_results_mapping.get(
        builtin_judge.GROUNDEDNESS.assessment_name
    )
    if groundedness_assessment is None:
        # Return default rating early if RCA does not exist
        return default_overall_rating
    elif _assessment_is_no(groundedness_assessment):
        return entities.Rating.value(
            categorical_value=entities.CategoricalRating.NO,
            rationale=constants.GROUNDEDNESS_FAILED_SUGGESTION,
        )

    correctness_assessment = assessment_results_mapping.get(
        builtin_judge.CORRECTNESS.assessment_name
    )
    relevance_to_query_assessment = assessment_results_mapping.get(
        builtin_judge.RELEVANCE_TO_QUERY.assessment_name
    )
    if correctness_assessment is None and relevance_to_query_assessment is None:
        # Return default rating early if RCA does not exist
        return default_overall_rating
    elif _assessment_is_no(correctness_assessment):
        return entities.Rating.value(
            categorical_value=entities.CategoricalRating.NO,
            rationale=constants.CORRECTNESS_FAILED_SUGGESTION,
        )
    elif _assessment_is_no(relevance_to_query_assessment):
        return entities.Rating.value(
            categorical_value=entities.CategoricalRating.NO,
            rationale=constants.RELEVANCE_TO_QUERY_FAILED_SUGGESTION,
        )

    safety_assessment = assessment_results_mapping.get(
        builtin_judge.HARMFULNESS.assessment_name
    )
    if safety_assessment is None:
        # Return default rating early if RCA does not exist
        return default_overall_rating
    elif _assessment_is_no(safety_assessment):
        return entities.Rating.value(
            categorical_value=entities.CategoricalRating.NO,
            rationale=constants.SAFETY_FAILED_SUGGESTION,
        )

    # Return default rating if all RCA judges pass
    return default_overall_rating


def _assessment_is_yes(assessment_result: Optional[entities.AssessmentResult]) -> bool:
    """
    Check if an assessment result is YES. For per-request assessments, the rating should be YES. For
    per-chunk assessments, all ratings should be YES, except for chunk relevance, for which at least
    one rating must be YES.

    :param assessment_result: The assessment result
    :return: True if the assessment result is YES. False if the assessment result is NO, UNKNOWN
     or the rating is None
    """
    if assessment_result is None:
        return False
    elif isinstance(assessment_result, entities.PerRequestAssessmentResult):
        return (
            assessment_result.rating.categorical_value == entities.CategoricalRating.YES
        )
    elif isinstance(assessment_result, entities.PerChunkAssessmentResult):
        posititional_ratings_are_yes = [
            rating.categorical_value == entities.CategoricalRating.YES
            for rating in assessment_result.positional_rating.values()
            if rating.error_code is None
        ]
        if (
            assessment_result.assessment_name
            == builtin_judge.CHUNK_RELEVANCE.assessment_name
        ):
            # For chunk relevance, the assessment is yes as long as a single relevant chunk is retrieved
            return any(posititional_ratings_are_yes)
        else:
            # For any other per-chunk assessment, all ratings must be yes
            return all(posititional_ratings_are_yes)
    else:
        raise error_utils.ValidationError(
            f"""Invalid assessment result type provided: {type(assessment_result)}. 
            Expected one of: [{type(entities.PerRequestAssessmentResult), type(entities.PerChunkAssessmentResult)}]"""
        )


def _assessment_is_no(assessment_result: Optional[entities.AssessmentResult]) -> bool:
    """
    Check if an assessment result is NO. For per-request assessments, the rating should be NO. For
    per-chunk assessments, at least one rating should be NO, except for chunk relevance, for which
    all ratings must be NO.

    :param assessment_result: The assessment result
    :return: True if the assessment result is NO or UNKNOWN. False if the assessment result is YES
     or the rating is None
    """
    return assessment_result is not None and not _assessment_is_yes(assessment_result)
