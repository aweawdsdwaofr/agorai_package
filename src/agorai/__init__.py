"""AgorAI: Democratic AI Through Multi-Agent Aggregation.

A Python library for building fair, unbiased AI systems through democratic
multi-agent opinion aggregation.
"""

__version__ = "0.2.0"

# Core aggregation
from agorai.aggregate import aggregate, list_methods

# Optional research modules (imported on demand to avoid heavy dependencies)
# Import queue: from agorai import queue
# Import visualization: from agorai import visualization

__all__ = ["aggregate", "list_methods", "__version__"]

# Convenience: Check if research modules are available
def has_queue():
    """Check if queue module is available."""
    try:
        import agorai.queue
        return True
    except ImportError:
        return False

def has_visualization():
    """Check if visualization module is available."""
    try:
        import agorai.visualization
        return True
    except ImportError:
        return False
