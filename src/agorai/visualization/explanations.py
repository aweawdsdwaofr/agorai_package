"""Natural language explanations for aggregation decisions."""

from typing import Dict, List, Any


def explain_decision(
    utilities: List[List[float]],
    method: str,
    winner: int,
    scores: List[float],
    **method_params
) -> str:
    """Generate natural language explanation for aggregation decision.

    Parameters
    ----------
    utilities : List[List[float]]
        Utility matrix
    method : str
        Aggregation method used
    winner : int
        Winning candidate index
    scores : List[float]
        Aggregated scores
    **method_params
        Method parameters used

    Returns
    -------
    str
        Natural language explanation

    Examples
    --------
    >>> utilities = [[0.8, 0.2], [0.3, 0.7]]
    >>> explanation = explain_decision(
    ...     utilities, "atkinson", winner=0,
    ...     scores=[0.5, 0.45], epsilon=1.0
    ... )
    >>> print(explanation)
    Candidate 0 won using the atkinson aggregation method...
    """
    n_agents = len(utilities)
    n_candidates = len(utilities[0])

    # Method-specific explanations
    explanations = {
        "majority": _explain_majority,
        "atkinson": _explain_atkinson,
        "maximin": _explain_maximin,
        "borda": _explain_borda,
        "score_centroid": _explain_centroid,
        "nash_bargaining": _explain_nash,
    }

    if method in explanations:
        return explanations[method](utilities, winner, scores, **method_params)
    else:
        return _explain_generic(method, utilities, winner, scores, **method_params)


def _explain_majority(utilities, winner, scores, **params):
    """Explain majority voting."""
    n_agents = len(utilities)
    votes = int(scores[winner])

    return f"""Candidate {winner} won by **majority voting** with {votes} out of {n_agents} votes.

**How it works:** Each agent votes for their highest-utility candidate. The candidate with the most votes wins.

**Properties:** Simple, intuitive, but can lead to "tyranny of the majority" where minority preferences are ignored.

**This result:** Candidate {winner} received the most votes ({votes}/{n_agents} = {votes/n_agents:.1%}).
"""


def _explain_atkinson(utilities, winner, scores, epsilon=1.0, **params):
    """Explain Atkinson aggregation."""
    n_candidates = len(utilities[0])

    interpretation = {
        0.0: "utilitarian (sum of utilities)",
        1.0: "geometric mean",
    }
    interp_str = interpretation.get(epsilon, f"inequality aversion level {epsilon}")

    return f"""Candidate {winner} won using **Atkinson aggregation** with ε={epsilon} ({interp_str}).

**How it works:** Atkinson method computes the "equally-distributed equivalent" (EDE) utility for each candidate. The EDE represents the utility level that, if given equally to all agents, would provide the same total welfare. Higher EDE = more fair distribution.

**Inequality aversion (ε):**
- ε=0: No aversion (utilitarian - just maximize total)
- ε=1: Moderate aversion (geometric mean - balance equality and efficiency)
- ε>1: Strong aversion (heavily penalize inequality)

**This result:** Candidate {winner} has the highest EDE score ({scores[winner]:.3f}). This means its utility distribution across agents is most equally distributed (given ε={epsilon}).

**Comparison:**
""" + "\n".join([
    f"- Candidate {i}: EDE = {scores[i]:.3f}" for i in range(n_candidates)
])


def _explain_maximin(utilities, winner, scores, **params):
    """Explain maximin (Rawlsian) aggregation."""
    n_candidates = len(utilities[0])

    worst_off = []
    for j in range(n_candidates):
        min_utility = min(u[j] for u in utilities)
        worst_off.append(min_utility)

    return f"""Candidate {winner} won using **Maximin (Rawlsian)** aggregation.

**How it works:** For each candidate, find the agent with the lowest utility (the "worst-off" agent). Choose the candidate that maximizes this minimum utility. This strongly protects minority interests.

**Philosophy:** Based on John Rawls' theory of justice - a society should be judged by how well it treats its worst-off members.

**This result:** Candidate {winner} has the highest minimum utility across all agents ({scores[winner]:.3f}).

**Worst-off agent utilities:**
""" + "\n".join([
    f"- Candidate {i}: min utility = {worst_off[i]:.3f}" for i in range(n_candidates)
])


def _explain_borda(utilities, winner, scores, **params):
    """Explain Borda count."""
    return f"""Candidate {winner} won using **Borda count** aggregation.

**How it works:** Each agent ranks candidates by utility. Points are awarded based on ranking (higher rank = more points). Candidate with most total points wins.

**Properties:** Considers full preference rankings (not just top choice), but can be manipulated by strategic voting.

**This result:** Candidate {winner} accumulated the highest Borda score ({scores[winner]:.1f} points).

**Borda scores:**
""" + "\n".join([
    f"- Candidate {i}: {scores[i]:.1f} points" for i in range(len(scores))
])


def _explain_centroid(utilities, winner, scores, **params):
    """Explain score centroid (average)."""
    return f"""Candidate {winner} won using **score centroid** (weighted average) aggregation.

**How it works:** Compute the weighted average of utilities for each candidate across all agents. Candidate with highest average wins.

**Properties:** Simple, efficient, treats all agents equally, but can be sensitive to outliers.

**This result:** Candidate {winner} has the highest average utility ({scores[winner]:.3f}).

**Average utilities:**
""" + "\n".join([
    f"- Candidate {i}: {scores[i]:.3f}" for i in range(len(scores))
])


def _explain_nash(utilities, winner, scores, **params):
    """Explain Nash bargaining."""
    return f"""Candidate {winner} won using **Nash bargaining** solution.

**How it works:** Maximize the product of utility gains (from a disagreement point) across all agents. This satisfies key game-theoretic fairness axioms (Pareto optimality, symmetry, independence of irrelevant alternatives).

**Philosophy:** Represents a fair compromise in cooperative bargaining scenarios.

**This result:** Candidate {winner} maximizes the Nash product ({scores[winner]:.2e}).

**Nash products:**
""" + "\n".join([
    f"- Candidate {i}: {scores[i]:.2e}" for i in range(len(scores))
])


def _explain_generic(method, utilities, winner, scores, **params):
    """Generic explanation for any method."""
    param_str = ", ".join([f"{k}={v}" for k, v in params.items()]) if params else "default parameters"

    return f"""Candidate {winner} won using **{method}** aggregation method.

**Parameters:** {param_str}

**Result:** Candidate {winner} achieved the highest score ({scores[winner]:.3f}).

**Scores:**
""" + "\n".join([
    f"- Candidate {i}: {scores[i]:.3f}" for i in range(len(scores))
])


def explain_method(method: str) -> str:
    """Explain what an aggregation method does and when to use it.

    Parameters
    ----------
    method : str
        Aggregation method name

    Returns
    -------
    str
        Description of method, properties, and use cases
    """
    descriptions = {
        "majority": """
**Majority Voting**

**Description:** Each agent votes for their top choice. Candidate with most votes wins.

**Properties:**
- ✓ Strategy-proof (under sincere voting)
- ✗ Violates Condorcet criterion
- ✗ Tyranny of majority risk
- ✓ Simple and intuitive

**When to use:**
- Binary or few choices
- Simple coordination needed
- All agents have equal weight
- Speed is important

**When NOT to use:**
- Need to consider preference intensity
- Minority protection required
- Complex fairness constraints
""",
        "atkinson": """
**Atkinson Aggregation**

**Description:** Computes equally-distributed equivalent (EDE) utility with parameterizable inequality aversion.

**Properties:**
- ✓ Monotonic
- ✓ Anonymous (agent-symmetric)
- ✓ Parameterizable fairness (ε)
- ✓ Based on welfare economics theory

**Parameters:**
- ε (epsilon): Inequality aversion
  - ε=0: Utilitarian (no aversion)
  - ε=1: Geometric mean (moderate)
  - ε→∞: Approaches maximin (strong)

**When to use:**
- Tunable fairness-efficiency tradeoff needed
- Welfare optimization
- Bias mitigation
- Cross-cultural decisions

**When NOT to use:**
- Need perfect equality (use maximin)
- Ordinal preferences only (use Borda/Condorcet)
""",
        "maximin": """
**Maximin (Rawlsian) Aggregation**

**Description:** Choose candidate that maximizes the minimum utility (helps worst-off agent most).

**Properties:**
- ✓ Strongly egalitarian
- ✓ Protects minorities
- ✗ Can be Pareto suboptimal
- ✓ Clear fairness interpretation

**Philosophy:**
Based on John Rawls' "veil of ignorance" - judge by worst outcome.

**When to use:**
- Fairness is paramount
- Minority protection required
- Bias mitigation (ensure no group harmed)
- High-stakes decisions

**When NOT to use:**
- Efficiency important
- Outlier agents present
- Need to balance multiple objectives
""",
        "borda": """
**Borda Count**

**Description:** Rank candidates, award points by position. Sum points across agents.

**Properties:**
- ✓ Monotonic
- ✓ Pareto efficient
- ✗ Vulnerable to strategic voting
- ✓ Considers full rankings

**When to use:**
- Preference ranking available
- Want to consider all preferences (not just top)
- Multi-agent coordination
- Complex preference structures

**When NOT to use:**
- Strategic voting concerns
- Only top preferences matter
- Need incentive compatibility
""",
    }

    return descriptions.get(method, f"No detailed description available for '{method}'.")
