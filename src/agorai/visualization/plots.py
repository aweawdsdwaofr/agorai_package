"""Plotting utilities for aggregation visualization."""

from typing import List, Optional
import warnings


def plot_utility_matrix(
    utilities: List[List[float]],
    agent_labels: Optional[List[str]] = None,
    candidate_labels: Optional[List[str]] = None,
    save_path: Optional[str] = None
):
    """Plot utility matrix as heatmap.

    Parameters
    ----------
    utilities : List[List[float]]
        Utility matrix (n_agents × n_candidates)
    agent_labels : Optional[List[str]]
        Labels for agents
    candidate_labels : Optional[List[str]]
        Labels for candidates
    save_path : Optional[str]
        Path to save plot

    Examples
    --------
    >>> utilities = [[0.8, 0.2], [0.3, 0.7]]
    >>> plot_utility_matrix(utilities, save_path="utilities.png")
    """
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        warnings.warn("matplotlib not installed. Install with: pip install matplotlib")
        return

    utilities_array = np.array(utilities)
    n_agents, n_candidates = utilities_array.shape

    if agent_labels is None:
        agent_labels = [f"Agent {i+1}" for i in range(n_agents)]
    if candidate_labels is None:
        candidate_labels = [f"Candidate {i}" for i in range(n_candidates)]

    fig, ax = plt.subplots(figsize=(max(6, n_candidates), max(4, n_agents)))

    im = ax.imshow(utilities_array, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)

    ax.set_xticks(np.arange(n_candidates))
    ax.set_yticks(np.arange(n_agents))
    ax.set_xticklabels(candidate_labels)
    ax.set_yticklabels(agent_labels)

    # Add text annotations
    for i in range(n_agents):
        for j in range(n_candidates):
            text = ax.text(j, i, f'{utilities_array[i, j]:.2f}',
                         ha="center", va="center", color="black", fontsize=10)

    ax.set_title("Utility Matrix")
    ax.set_xlabel("Candidates")
    ax.set_ylabel("Agents")

    plt.colorbar(im, ax=ax, label="Utility")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()

    plt.close()


def plot_aggregation_comparison(
    utilities: List[List[float]],
    methods: List[str],
    highlight_differences: bool = True,
    save_path: Optional[str] = None,
    **method_params
):
    """Compare aggregation methods side-by-side.

    Parameters
    ----------
    utilities : List[List[float]]
        Utility matrix
    methods : List[str]
        List of aggregation methods to compare
    highlight_differences : bool
        Whether to highlight different winners
    save_path : Optional[str]
        Path to save plot
    **method_params
        Parameters for aggregation methods
    """
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        warnings.warn("matplotlib not installed. Install with: pip install matplotlib")
        return

    from agorai.aggregate import aggregate

    n_methods = len(methods)
    fig, axes = plt.subplots(1, n_methods, figsize=(5*n_methods, 4))

    if n_methods == 1:
        axes = [axes]

    winners = []
    for idx, method in enumerate(methods):
        result = aggregate(utilities, method=method, **method_params)
        winner = result['winner']
        scores = result['scores']
        winners.append(winner)

        ax = axes[idx]
        x = np.arange(len(scores))
        bars = ax.bar(x, scores)

        # Highlight winner
        bars[winner].set_color('green')

        ax.set_title(f"{method}\n(Winner: {winner})")
        ax.set_xlabel("Candidate")
        ax.set_ylabel("Score")
        ax.set_xticks(x)

    # Highlight if different winners
    if highlight_differences and len(set(winners)) > 1:
        fig.suptitle("⚠ Different Winners!", fontsize=14, color='red')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()

    plt.close()


def plot_fairness_tradeoffs(
    utilities: List[List[float]],
    methods: List[str],
    x_axis: str = "social_welfare",
    y_axis: str = "gini_coefficient",
    pareto_frontier: bool = False,
    save_path: Optional[str] = None
):
    """Plot fairness-efficiency tradeoffs.

    Parameters
    ----------
    utilities : List[List[float]]
        Utility matrix
    methods : List[str]
        List of aggregation methods
    x_axis : str
        Metric for x-axis (default: social_welfare)
    y_axis : str
        Metric for y-axis (default: gini_coefficient)
    pareto_frontier : bool
        Whether to draw Pareto frontier
    save_path : Optional[str]
        Path to save plot
    """
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        warnings.warn("matplotlib not installed. Install with: pip install matplotlib")
        return

    from agorai.aggregate import aggregate
    from agorai.benchmarks.metrics import calculate_all_metrics

    x_values = []
    y_values = []
    labels = []

    for method in methods:
        result = aggregate(utilities, method=method)
        winner = result['winner']
        scores = result['scores']

        metrics = calculate_all_metrics(utilities, scores, winner)

        # Extract x and y values based on requested metrics
        if x_axis == "social_welfare":
            x = metrics['efficiency']['social_welfare']
        elif x_axis == "utilitarian_welfare":
            x = metrics['efficiency']['utilitarian_welfare']
        else:
            x = 0

        if y_axis == "gini_coefficient":
            y = metrics['fairness']['gini_coefficient']
        elif y_axis == "atkinson_index":
            y = metrics['fairness']['atkinson_index']
        else:
            y = 0

        x_values.append(x)
        y_values.append(y)
        labels.append(method)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Scatter plot
    ax.scatter(x_values, y_values, s=100, alpha=0.6)

    # Add labels
    for i, label in enumerate(labels):
        ax.annotate(label, (x_values[i], y_values[i]),
                   xytext=(5, 5), textcoords='offset points')

    ax.set_xlabel(x_axis.replace('_', ' ').title())
    ax.set_ylabel(y_axis.replace('_', ' ').title())
    ax.set_title("Fairness-Efficiency Tradeoffs")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()

    plt.close()
