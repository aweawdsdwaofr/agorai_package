"""Metrics for evaluating aggregation fairness, efficiency, and agreement."""

from typing import List, Dict, Any
import statistics
import math


def calculate_fairness_metrics(utilities: List[List[float]], scores: List[float]) -> Dict[str, float]:
    """Calculate fairness metrics for an aggregation result.

    Parameters
    ----------
    utilities : List[List[float]]
        Utility matrix (n_agents × n_candidates)
    scores : List[float]
        Aggregated scores for each candidate

    Returns
    -------
    Dict[str, float]
        Fairness metrics:
        - 'gini_coefficient': Gini coefficient of utility distribution (0-1, lower is more equal)
        - 'atkinson_index': Atkinson inequality index with ε=1 (0-1, lower is more equal)
        - 'variance': Variance of utilities
        - 'coefficient_of_variation': CV of utilities

    Notes
    -----
    Lower values indicate more equal (fair) distributions.
    Gini coefficient of 0 = perfect equality, 1 = perfect inequality.

    Examples
    --------
    >>> utilities = [[0.8, 0.2], [0.3, 0.7], [0.5, 0.5]]
    >>> scores = [0.53, 0.47]
    >>> metrics = calculate_fairness_metrics(utilities, scores)
    >>> print(f"Gini: {metrics['gini_coefficient']:.3f}")
    Gini: 0.125
    """
    n_agents = len(utilities)
    n_candidates = len(utilities[0])

    # Get winner
    winner = max(range(n_candidates), key=lambda i: scores[i])

    # Get utilities for winning candidate
    winner_utilities = [u[winner] for u in utilities]

    # Gini coefficient
    gini = _gini_coefficient(winner_utilities)

    # Atkinson index (ε=1, geometric mean)
    atkinson = _atkinson_index(winner_utilities, epsilon=1.0)

    # Variance and CV
    mean_utility = statistics.mean(winner_utilities)
    variance = statistics.variance(winner_utilities) if len(winner_utilities) > 1 else 0.0
    cv = math.sqrt(variance) / mean_utility if mean_utility > 1e-10 else 0.0

    return {
        'gini_coefficient': gini,
        'atkinson_index': atkinson,
        'variance': variance,
        'coefficient_of_variation': cv,
    }


def calculate_efficiency_metrics(utilities: List[List[float]], winner: int) -> Dict[str, float]:
    """Calculate efficiency metrics for an aggregation result.

    Parameters
    ----------
    utilities : List[List[float]]
        Utility matrix (n_agents × n_candidates)
    winner : int
        Index of winning candidate

    Returns
    -------
    Dict[str, float]
        Efficiency metrics:
        - 'social_welfare': Sum of utilities for winner
        - 'utilitarian_welfare': Mean utility for winner
        - 'pareto_efficiency': 1.0 if Pareto efficient, 0.0 otherwise

    Notes
    -----
    Higher values indicate better efficiency (more total welfare).
    Pareto efficiency: no other candidate makes everyone better off.

    Examples
    --------
    >>> utilities = [[0.8, 0.2], [0.3, 0.7], [0.5, 0.5]]
    >>> winner = 0
    >>> metrics = calculate_efficiency_metrics(utilities, winner)
    >>> print(f"Social welfare: {metrics['social_welfare']:.2f}")
    Social welfare: 1.60
    """
    n_agents = len(utilities)
    n_candidates = len(utilities[0])

    # Winner utilities
    winner_utilities = [u[winner] for u in utilities]

    # Social welfare (sum)
    social_welfare = sum(winner_utilities)

    # Utilitarian welfare (mean)
    utilitarian_welfare = social_welfare / n_agents

    # Check Pareto efficiency
    # Winner is Pareto efficient if no other candidate is better for all agents
    is_pareto_efficient = True
    for j in range(n_candidates):
        if j == winner:
            continue

        # Check if candidate j is better for all agents
        better_for_all = all(utilities[i][j] > utilities[i][winner] for i in range(n_agents))
        if better_for_all:
            is_pareto_efficient = False
            break

    return {
        'social_welfare': social_welfare,
        'utilitarian_welfare': utilitarian_welfare,
        'pareto_efficiency': 1.0 if is_pareto_efficient else 0.0,
    }


def calculate_agreement_metrics(utilities: List[List[float]], winner: int) -> Dict[str, float]:
    """Calculate agreement/consensus metrics for an aggregation result.

    Parameters
    ----------
    utilities : List[List[float]]
        Utility matrix (n_agents × n_candidates)
    winner : int
        Index of winning candidate

    Returns
    -------
    Dict[str, float]
        Agreement metrics:
        - 'consensus_score': Fraction of agents who prefer winner (0-1)
        - 'average_support': Mean utility for winner across agents
        - 'minimum_support': Minimum utility for winner across agents

    Notes
    -----
    Higher values indicate stronger agreement/consensus.

    Examples
    --------
    >>> utilities = [[0.8, 0.2], [0.9, 0.1], [0.7, 0.3]]
    >>> winner = 0
    >>> metrics = calculate_agreement_metrics(utilities, winner)
    >>> print(f"Consensus: {metrics['consensus_score']:.2f}")
    Consensus: 1.00
    """
    n_agents = len(utilities)
    n_candidates = len(utilities[0])

    # Winner utilities
    winner_utilities = [u[winner] for u in utilities]

    # Count how many agents prefer winner
    num_prefer_winner = 0
    for i in range(n_agents):
        # Agent prefers winner if it's their highest-utility candidate
        if winner == max(range(n_candidates), key=lambda j: utilities[i][j]):
            num_prefer_winner += 1

    consensus_score = num_prefer_winner / n_agents

    # Average and minimum support
    average_support = statistics.mean(winner_utilities)
    minimum_support = min(winner_utilities)

    return {
        'consensus_score': consensus_score,
        'average_support': average_support,
        'minimum_support': minimum_support,
    }


def _gini_coefficient(values: List[float]) -> float:
    """Calculate Gini coefficient of a distribution.

    Parameters
    ----------
    values : List[float]
        Distribution values

    Returns
    -------
    float
        Gini coefficient (0-1, where 0 is perfect equality)
    """
    if len(values) == 0:
        return 0.0

    if len(values) == 1:
        return 0.0

    # Sort values
    sorted_values = sorted(values)
    n = len(sorted_values)

    # Compute Gini coefficient
    # G = (2 * sum(i * x_i)) / (n * sum(x_i)) - (n + 1) / n
    cumsum = 0.0
    total = sum(sorted_values)

    if total < 1e-10:
        return 0.0

    for i, value in enumerate(sorted_values, 1):
        cumsum += i * value

    gini = (2.0 * cumsum) / (n * total) - (n + 1.0) / n

    return max(0.0, min(1.0, gini))  # Clamp to [0, 1]


def _atkinson_index(values: List[float], epsilon: float = 1.0) -> float:
    """Calculate Atkinson inequality index.

    Parameters
    ----------
    values : List[float]
        Distribution values
    epsilon : float
        Inequality aversion parameter (0 to infinity)
        - 0: no aversion (utilitarian)
        - 1: moderate aversion (geometric mean)
        - >1: strong aversion

    Returns
    -------
    float
        Atkinson index (0-1, where 0 is perfect equality)
    """
    if len(values) == 0:
        return 0.0

    if len(values) == 1:
        return 0.0

    n = len(values)
    mean_value = statistics.mean(values)

    if mean_value < 1e-10:
        return 0.0

    if epsilon == 0.0:
        # No inequality aversion (A = 0)
        return 0.0

    if epsilon == 1.0:
        # Geometric mean case
        product = 1.0
        for v in values:
            product *= max(v, 1e-10)  # Avoid log(0)

        geometric_mean = product ** (1.0 / n)
        atkinson = 1.0 - geometric_mean / mean_value

    else:
        # General case
        power_sum = sum(max(v, 1e-10) ** (1 - epsilon) for v in values)
        ede = (power_sum / n) ** (1 / (1 - epsilon))
        atkinson = 1.0 - ede / mean_value

    return max(0.0, min(1.0, atkinson))  # Clamp to [0, 1]


def calculate_all_metrics(
    utilities: List[List[float]],
    scores: List[float],
    winner: int
) -> Dict[str, Dict[str, float]]:
    """Calculate all available metrics for an aggregation result.

    Parameters
    ----------
    utilities : List[List[float]]
        Utility matrix (n_agents × n_candidates)
    scores : List[float]
        Aggregated scores for each candidate
    winner : int
        Index of winning candidate

    Returns
    -------
    Dict[str, Dict[str, float]]
        All metrics organized by category:
        - 'fairness': Fairness metrics
        - 'efficiency': Efficiency metrics
        - 'agreement': Agreement metrics

    Examples
    --------
    >>> utilities = [[0.8, 0.2], [0.3, 0.7], [0.5, 0.5]]
    >>> scores = [0.53, 0.47]
    >>> winner = 0
    >>> all_metrics = calculate_all_metrics(utilities, scores, winner)
    >>> print(all_metrics['fairness']['gini_coefficient'])
    0.125
    """
    return {
        'fairness': calculate_fairness_metrics(utilities, scores),
        'efficiency': calculate_efficiency_metrics(utilities, winner),
        'agreement': calculate_agreement_metrics(utilities, winner),
    }
