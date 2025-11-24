"""Queue-based batch processing for aggregation methods.

This module enables processing multiple aggregation requests from files,
useful for:
- Production batch processing
- Testing on datasets
- Evaluating multiple scenarios
- Comparing methods across many cases
"""

from agorai.queue.core import (
    load_requests_from_file,
    process_single_request,
    process_queue,
    compare_methods_on_queue,
    SIMPLE_VOTING_EXAMPLE,
)

from agorai.queue.metrics import (
    calculate_fairness_metrics,
    calculate_efficiency_metrics,
    calculate_agreement_metrics,
)

__all__ = [
    "load_requests_from_file",
    "process_single_request",
    "process_queue",
    "compare_methods_on_queue",
    "SIMPLE_VOTING_EXAMPLE",
    "calculate_fairness_metrics",
    "calculate_efficiency_metrics",
    "calculate_agreement_metrics",
]
