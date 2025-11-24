"""Visualization tools for aggregation results.

Provides plotting and explanation utilities for aggregation methods.
"""

from agorai.visualization.plots import (
    plot_utility_matrix,
    plot_aggregation_comparison,
    plot_fairness_tradeoffs,
)

from agorai.visualization.explanations import (
    explain_decision,
    explain_method,
)

__all__ = [
    "plot_utility_matrix",
    "plot_aggregation_comparison",
    "plot_fairness_tradeoffs",
    "explain_decision",
    "explain_method",
]
