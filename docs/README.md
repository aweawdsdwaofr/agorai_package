# AgorAI Documentation

Complete documentation for the AgorAI package.

## Quick Links

- [Installation Guide](#installation)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Guides](#guides)
- [Examples](#examples)

---

## Installation

### Basic Installation

```bash
pip install agorai
```

### With Research Features

```bash
pip install agorai[research]  # Queue processing + visualization
```

### Complete Installation

```bash
pip install agorai[all]  # All features
```

See [Configuration Guide](configuration.md) for detailed installation options.

---

## Quick Start

### 1. Pure Aggregation

```python
from agorai.aggregate import aggregate

utilities = [[0.8, 0.2], [0.3, 0.7], [0.5, 0.5]]
result = aggregate(utilities, method="atkinson", epsilon=1.0)
print(f"Winner: Candidate {result['winner']}")
```

### 2. Queue Processing

```python
from agorai.queue import process_queue

results = process_queue(
    requests_file="production_data.json",
    method="atkinson",
    metrics=["fairness", "efficiency"],
    epsilon=1.0
)
print(f"Processed {results['num_requests']} requests")
```

### 3. LLM Synthesis

```python
from agorai.synthesis import Agent, synthesize

agents = [
    Agent(provider="openai", model="gpt-4"),
    Agent(provider="anthropic", model="claude-3-5-sonnet-20241022"),
]

result = synthesize(
    prompt="Should we implement this feature?",
    agents=agents,
    aggregation_method="majority"
)
```

---

## API Reference

### Core Aggregation

**[aggregate.md](aggregate.md)** - Complete aggregation API
- `aggregate()` - Main aggregation function
- `list_methods()` - List available methods
- `register_method()` - Add custom methods
- 14+ built-in aggregation methods

### Queue Processing

**[queue.md](queue.md)** - Batch processing from files
- `load_requests_from_file()` - Load requests from JSON
- `process_single_request()` - Process one request
- `process_queue()` - Process multiple requests
- `compare_methods_on_queue()` - Compare methods
- Metrics calculation (fairness, efficiency, agreement)

### Visualization

**[visualization.md](visualization.md)** - Plots and explanations
- `plot_utility_matrix()` - Heatmap visualization
- `plot_aggregation_comparison()` - Method comparison
- `plot_fairness_tradeoffs()` - Fairness vs efficiency
- `explain_decision()` - Natural language explanations
- `explain_method()` - Method documentation

---

## Guides

### User Guides

1. **[Configuration Guide](configuration.md)** ⭐ NEW
   - Installation options
   - Environment variables
   - LLM provider configuration
   - Default settings
   - Production setup

2. **[Queue Processing Guide](queue.md)**
   - File format specification
   - Processing requests
   - Comparing methods
   - Use cases and examples

3. **[Visualization Guide](visualization.md)**
   - Creating plots
   - Natural language explanations
   - Customization
   - Best practices

### Developer Guides

4. **[Extending Guide](extending.md)** ⭐ NEW
   - Adding new aggregation methods
   - Configuring LLM providers
   - Creating custom metrics
   - Extending the queue system
   - Custom visualization
   - Integration patterns (FastAPI, Django, Celery)

5. **[Aggregation API](aggregate.md)**
   - Method reference
   - Parameters and return values
   - Examples for each method

---

## Guides by Topic

### Getting Started
- ✅ [README](../README.md) - Package overview
- ✅ [Configuration](configuration.md) - Setup and configuration
- ✅ [Quick Start Examples](../README.md#quick-start)

### Core Features
- ✅ [Aggregation Methods](aggregate.md) - All 14+ methods
- ✅ [Queue Processing](queue.md) - Batch operations
- ✅ [Visualization](visualization.md) - Plots and explanations

### Advanced Topics
- ✅ [Extending AgorAI](extending.md) - Customization
- ✅ [Integration Patterns](extending.md#integration-patterns) - Web APIs, async
- 📝 [Performance Optimization](performance.md) - Coming soon

### Reference
- ✅ [Aggregation API](aggregate.md) - Complete reference
- ✅ [Queue API](queue.md) - Complete reference
- ✅ [Visualization API](visualization.md) - Complete reference
- ✅ [Metrics Reference](queue.md#metrics) - All metrics explained

---

## Examples

### Code Examples

Located in `examples/` directory:

1. **[production_requests.json](../examples/production_requests.json)**
   - Example request file for queue processing
   - Content moderation use case
   - Shows file format and structure

2. **Jupyter Notebooks** (in `notebooks/`)
   - `agorai_demo.ipynb` - Interactive tutorial
   - Covers all major features

### Use Case Examples

#### Production Batch Processing
```python
from agorai.queue import process_queue

# Process daily content moderation decisions
results = process_queue(
    requests_file="daily_moderation.json",
    method="atkinson",
    metrics=["fairness", "efficiency"],
    epsilon=1.0
)

for item in results['results']:
    action = ["Approve", "Reject", "Escalate"][item['winner']]
    print(f"{item['item_id']}: {action}")
```

#### Method Comparison
```python
from agorai.queue import compare_methods_on_queue

# Find best method for your use case
comparison = compare_methods_on_queue(
    requests_file="test_dataset.json",
    methods=["majority", "atkinson", "maximin", "nash_bargaining"],
    metrics=["fairness", "efficiency"]
)

print("Fairest method:", comparison['rankings']['fairness_gini_coefficient'][0])
```

#### Custom Aggregation Method
```python
from agorai.aggregate import register_method, aggregate
import numpy as np

def harmonic_mean(utilities, **params):
    utils = np.array(utilities)
    scores = []
    for col in utils.T:
        scores.append(len(col) / np.sum(1.0 / np.maximum(col, 0.1)))
    return {'winner': int(np.argmax(scores)), 'scores': scores, 'method': 'harmonic'}

register_method('harmonic', harmonic_mean)
result = aggregate([[0.8, 0.2], [0.6, 0.4]], method='harmonic')
```

---

## Documentation Structure

```
docs/
├── README.md                    # This file - documentation index
├── configuration.md             # Setup and configuration ⭐ NEW
├── extending.md                 # Developer guide for customization ⭐ NEW
├── aggregate.md                 # Aggregation API reference
├── queue.md                     # Queue processing guide
└── visualization.md             # Visualization guide
```

---

## Aggregation Methods Reference

### Social Choice Methods
- **majority** - Simple plurality voting
- **weighted_plurality** - Weighted votes
- **borda** - Borda count (ranking-based)
- **schulze_condorcet** - Condorcet method
- **approval_voting** - Approval-based
- **supermajority** - Requires threshold
- **quadratic_voting** - Quadratic weights

### Welfare Economics Methods
- **maximin** - Rawlsian (protect worst-off)
- **atkinson** - Inequality-averse (parameterized)
- **nash_bargaining** - Game-theoretic fair

### Machine Learning Methods
- **score_centroid** - Average scores
- **robust_median** - Median-based
- **consensus** - Agreement-maximizing

### Hybrid Methods
- **veto_hybrid** - Combines multiple methods

See [Aggregation API](aggregate.md) for complete reference.

---

## Metrics Reference

### Fairness Metrics (lower is better)
- **Gini coefficient** - Classic inequality measure (0-1)
- **Atkinson index** - Parameterizable inequality (0-1)
- **Variance** - Statistical spread
- **Coefficient of variation** - Normalized variance

### Efficiency Metrics (higher is better)
- **Social welfare** - Sum of utilities
- **Utilitarian welfare** - Mean utility
- **Pareto efficiency** - No dominated alternatives (0 or 1)

### Agreement Metrics (higher is better)
- **Consensus score** - Fraction agreeing (0-1)
- **Average support** - Mean utility for winner (0-1)
- **Minimum support** - Worst-case utility (0-1)

See [Queue Guide - Metrics](queue.md#metrics) for details.

---

## FAQ

### How do I add a custom aggregation method?

See [Extending Guide - Adding Methods](extending.md#adding-new-aggregation-methods)

### How do I change the default LLM provider?

See [Configuration Guide - LLM Providers](configuration.md#llm-provider-configuration)

### How do I process production data in batches?

See [Queue Processing Guide](queue.md)

### How do I create custom visualizations?

See [Extending Guide - Custom Visualization](extending.md#custom-visualization)

### How do I integrate with FastAPI/Django?

See [Extending Guide - Integration Patterns](extending.md#integration-patterns)

---

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for:
- Code style guidelines
- Testing requirements
- Pull request process
- Development setup

---

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/agorai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/agorai/discussions)
- **Email**: samuel.schlenker@example.com

---

## Version History

- **v0.2.0** (2025-11-24): Queue processing + visualization modules
- **v0.1.0** (2024-11-20): Initial release

See [CHANGELOG.md](../CHANGELOG.md) for complete history.

---

## License

Custom Research and Non-Commercial License

Free for:
- Academic research
- Education
- Personal use

Commercial use requires agreement. See [LICENSE](../LICENSE) for details.

---

**Happy aggregating! 🚀**
