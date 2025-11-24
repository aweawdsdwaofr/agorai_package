"""Queue-based batch processing for aggregation methods.

This module allows processing multiple aggregation requests from files,
enabling batch operations on production data, test datasets, or any
collection of decision-making scenarios.
"""

from typing import Dict, List, Any, Optional, Union
import json
import os
from pathlib import Path
import statistics

from agorai.aggregate import aggregate, list_methods
from agorai.queue.metrics import (
    calculate_fairness_metrics,
    calculate_efficiency_metrics,
    calculate_agreement_metrics,
)


def load_requests_from_file(file_path: str) -> Dict[str, Any]:
    """Load aggregation requests from a JSON file.

    Parameters
    ----------
    file_path : str
        Path to JSON file containing requests

    Returns
    -------
    Dict[str, Any]
        Request data including:
        - 'name': Request set name
        - 'description': Description (optional)
        - 'items': List of aggregation requests with utilities
        - 'metadata': Additional information (optional)

    Examples
    --------
    >>> requests = load_requests_from_file("production_batch.json")
    >>> print(f"Loaded {len(requests['items'])} requests")
    Loaded 50 requests

    File Format
    -----------
    {
        "name": "content_moderation_batch",
        "description": "Daily content moderation decisions",
        "items": [
            {
                "id": "item_001",
                "utilities": [[0.8, 0.2], [0.3, 0.7]],
                "ground_truth": 0,  // optional
                "metadata": {...}   // optional
            },
            ...
        ],
        "metadata": {
            "date": "2025-11-24",
            "source": "production"
        }
    }
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(path, 'r') as f:
        data = json.load(f)

    # Validate required fields
    if 'items' not in data:
        raise ValueError("File must contain 'items' field with list of requests")

    return data


def process_single_request(
    utilities: List[List[float]],
    method: str = "majority",
    metrics: Optional[List[str]] = None,
    **method_params
) -> Dict[str, Any]:
    """Process a single aggregation request.

    Parameters
    ----------
    utilities : List[List[float]]
        Utility matrix (n_agents × n_candidates)
    method : str
        Aggregation method name
    metrics : Optional[List[str]]
        Metrics to compute: ['fairness', 'efficiency', 'agreement']
    **method_params
        Parameters for the aggregation method

    Returns
    -------
    Dict[str, Any]
        Result containing:
        - 'winner': Winning candidate index
        - 'scores': Aggregated scores
        - 'method': Method used
        - 'metrics': Computed metrics (if requested)

    Examples
    --------
    >>> utilities = [[0.8, 0.2], [0.3, 0.7], [0.5, 0.5]]
    >>> result = process_single_request(utilities, method="atkinson", epsilon=1.0)
    >>> print(f"Winner: Candidate {result['winner']}")
    Winner: Candidate 0
    """
    if metrics is None:
        metrics = []

    # Run aggregation
    agg_result = aggregate(utilities, method=method, **method_params)

    result = {
        'winner': agg_result['winner'],
        'scores': agg_result['scores'],
        'method': method,
        'method_params': method_params,
    }

    # Add requested metrics
    if metrics:
        result['metrics'] = {}

        if 'fairness' in metrics:
            result['metrics']['fairness'] = calculate_fairness_metrics(
                utilities, agg_result['scores']
            )

        if 'efficiency' in metrics:
            result['metrics']['efficiency'] = calculate_efficiency_metrics(
                utilities, agg_result['winner']
            )

        if 'agreement' in metrics:
            result['metrics']['agreement'] = calculate_agreement_metrics(
                utilities, agg_result['winner']
            )

    return result


def process_queue(
    requests_file: str,
    method: str = "majority",
    metrics: Optional[List[str]] = None,
    **method_params
) -> Dict[str, Any]:
    """Process a queue of aggregation requests from a file.

    Parameters
    ----------
    requests_file : str
        Path to JSON file with requests
    method : str
        Aggregation method to use
    metrics : Optional[List[str]]
        Metrics to compute for each request
    **method_params
        Parameters for the aggregation method

    Returns
    -------
    Dict[str, Any]
        Processing results containing:
        - 'source_file': Input file path
        - 'method': Method used
        - 'num_requests': Number of requests processed
        - 'results': List of results for each request
        - 'summary': Aggregate statistics (if metrics computed)

    Examples
    --------
    >>> results = process_queue(
    ...     "production_data.json",
    ...     method="atkinson",
    ...     metrics=["fairness", "efficiency"],
    ...     epsilon=1.0
    ... )
    >>> print(f"Processed {results['num_requests']} requests")
    >>> print(f"Average Gini: {results['summary']['fairness']['gini_coefficient']:.3f}")
    """
    # Load requests from file
    requests_data = load_requests_from_file(requests_file)
    items = requests_data['items']

    # Process each request
    results = []
    for item in items:
        utilities = item['utilities']

        # Process request
        result = process_single_request(
            utilities,
            method=method,
            metrics=metrics,
            **method_params
        )

        # Add item metadata
        result['item_id'] = item.get('id', f"item_{len(results)}")
        result['ground_truth'] = item.get('ground_truth')

        # Check correctness if ground truth provided
        if result['ground_truth'] is not None:
            result['is_correct'] = result['winner'] == result['ground_truth']

        results.append(result)

    # Compute summary statistics if metrics requested
    summary = {}
    if metrics and results:
        summary = _compute_summary(results, metrics)

    return {
        'source_file': requests_file,
        'source_name': requests_data.get('name', 'unknown'),
        'method': method,
        'method_params': method_params,
        'num_requests': len(results),
        'results': results,
        'summary': summary,
    }


def compare_methods_on_queue(
    requests_file: str,
    methods: List[Union[str, Dict[str, Any]]],
    metrics: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Compare multiple aggregation methods on the same queue of requests.

    Parameters
    ----------
    requests_file : str
        Path to JSON file with requests
    methods : List[Union[str, Dict[str, Any]]]
        List of method names or dicts with {'name': str, 'params': dict}
    metrics : Optional[List[str]]
        Metrics to compute

    Returns
    -------
    Dict[str, Any]
        Comparison results containing:
        - 'source_file': Input file
        - 'methods': Results for each method
        - 'rankings': Methods ranked by each metric

    Examples
    --------
    >>> comparison = compare_methods_on_queue(
    ...     "daily_decisions.json",
    ...     methods=["majority", "atkinson", "maximin"],
    ...     metrics=["fairness", "efficiency"]
    ... )
    >>> print("Fairness rankings:", comparison['rankings']['fairness_gini_coefficient'])
    """
    if metrics is None:
        metrics = ['fairness', 'efficiency', 'agreement']

    method_results = []

    for method_spec in methods:
        # Parse method specification
        if isinstance(method_spec, str):
            method_name = method_spec
            method_params = {}
        else:
            method_name = method_spec['name']
            method_params = method_spec.get('params', {})

        # Process queue with this method
        result = process_queue(
            requests_file,
            method=method_name,
            metrics=metrics,
            **method_params
        )

        method_results.append(result)

    # Compute rankings
    rankings = {}
    if metrics and method_results:
        rankings = _compute_rankings(method_results, metrics)

    return {
        'source_file': requests_file,
        'num_methods': len(methods),
        'methods': method_results,
        'rankings': rankings,
    }


def _compute_summary(results: List[Dict[str, Any]], metrics: List[str]) -> Dict[str, Any]:
    """Compute summary statistics across all results."""
    summary = {}

    # Accuracy (if ground truth available)
    with_gt = [r for r in results if r.get('ground_truth') is not None]
    if with_gt:
        correct = sum(1 for r in with_gt if r.get('is_correct', False))
        summary['accuracy'] = correct / len(with_gt)
        summary['num_with_ground_truth'] = len(with_gt)

    # Aggregate metrics
    if 'fairness' in metrics:
        fairness_data = [r['metrics']['fairness'] for r in results if 'metrics' in r]
        if fairness_data:
            summary['fairness'] = {
                'gini_coefficient': statistics.mean(m['gini_coefficient'] for m in fairness_data),
                'atkinson_index': statistics.mean(m['atkinson_index'] for m in fairness_data),
                'variance': statistics.mean(m['variance'] for m in fairness_data),
                'coefficient_of_variation': statistics.mean(m['coefficient_of_variation'] for m in fairness_data),
            }

    if 'efficiency' in metrics:
        efficiency_data = [r['metrics']['efficiency'] for r in results if 'metrics' in r]
        if efficiency_data:
            summary['efficiency'] = {
                'social_welfare': statistics.mean(m['social_welfare'] for m in efficiency_data),
                'utilitarian_welfare': statistics.mean(m['utilitarian_welfare'] for m in efficiency_data),
                'pareto_efficiency': statistics.mean(m['pareto_efficiency'] for m in efficiency_data),
            }

    if 'agreement' in metrics:
        agreement_data = [r['metrics']['agreement'] for r in results if 'metrics' in r]
        if agreement_data:
            summary['agreement'] = {
                'consensus_score': statistics.mean(m['consensus_score'] for m in agreement_data),
                'average_support': statistics.mean(m['average_support'] for m in agreement_data),
                'minimum_support': statistics.mean(m['minimum_support'] for m in agreement_data),
            }

    return summary


def _compute_rankings(method_results: List[Dict[str, Any]], metrics: List[str]) -> Dict[str, List[str]]:
    """Compute rankings of methods by each metric."""
    rankings = {}

    # Accuracy ranking
    with_accuracy = [(r['method'], r['summary'].get('accuracy', 0))
                     for r in method_results if 'accuracy' in r['summary']]
    if with_accuracy:
        sorted_acc = sorted(with_accuracy, key=lambda x: x[1], reverse=True)
        rankings['accuracy'] = [method for method, _ in sorted_acc]

    # Fairness rankings (lower is better for Gini)
    if 'fairness' in metrics:
        for metric_name in ['gini_coefficient', 'atkinson_index', 'variance', 'coefficient_of_variation']:
            metric_values = [
                (r['method'], r['summary']['fairness'][metric_name])
                for r in method_results if 'fairness' in r['summary']
            ]
            if metric_values:
                sorted_values = sorted(metric_values, key=lambda x: x[1])
                rankings[f'fairness_{metric_name}'] = [method for method, _ in sorted_values]

    # Efficiency rankings (higher is better)
    if 'efficiency' in metrics:
        for metric_name in ['social_welfare', 'utilitarian_welfare', 'pareto_efficiency']:
            metric_values = [
                (r['method'], r['summary']['efficiency'][metric_name])
                for r in method_results if 'efficiency' in r['summary']
            ]
            if metric_values:
                sorted_values = sorted(metric_values, key=lambda x: x[1], reverse=True)
                rankings[f'efficiency_{metric_name}'] = [method for method, _ in sorted_values]

    # Agreement rankings (higher is better)
    if 'agreement' in metrics:
        for metric_name in ['consensus_score', 'average_support', 'minimum_support']:
            metric_values = [
                (r['method'], r['summary']['agreement'][metric_name])
                for r in method_results if 'agreement' in r['summary']
            ]
            if metric_values:
                sorted_values = sorted(metric_values, key=lambda x: x[1], reverse=True)
                rankings[f'agreement_{metric_name}'] = [method for method, _ in sorted_values]

    return rankings


# Built-in example datasets (optional, for testing)
SIMPLE_VOTING_EXAMPLE = {
    'name': 'simple_voting',
    'description': 'Simple voting scenarios for testing',
    'items': [
        {
            'id': 'majority_clear',
            'utilities': [[1.0, 0.0], [1.0, 0.0], [1.0, 0.0]],
            'ground_truth': 0,
            'description': 'Clear 3-0 majority',
        },
        {
            'id': 'split_decision',
            'utilities': [[0.8, 0.2], [0.7, 0.3], [0.3, 0.7]],
            'ground_truth': 0,
            'description': '2-1 split decision',
        },
        {
            'id': 'equal_utilities',
            'utilities': [[0.5, 0.5], [0.5, 0.5], [0.5, 0.5]],
            'ground_truth': None,
            'description': 'All agents indifferent',
        },
        {
            'id': 'extreme_inequality',
            'utilities': [[0.9, 0.1], [0.1, 0.9], [0.1, 0.9]],
            'ground_truth': 1,
            'description': 'One agent vs. two (minority protection test)',
        },
        {
            'id': 'moderate_prefs',
            'utilities': [[0.6, 0.4], [0.55, 0.45], [0.45, 0.55]],
            'ground_truth': 0,
            'description': 'Moderate preference distribution',
        },
    ],
    'metadata': {
        'num_candidates': 2,
        'num_agents': 3,
        'domain': 'voting',
        'purpose': 'testing',
    }
}
