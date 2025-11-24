# AgorAI Notebooks

Interactive Jupyter notebooks demonstrating AgorAI features.

## Available Notebooks

### 1. agorai_demo.ipynb - Complete Demo

**What it covers:**
- ✅ Core aggregation (14+ methods)
- ✅ Benchmarking with scientific metrics
- ✅ Visualization (plots + explanations)
- ✅ Real-world example (content moderation)
- ✅ Parameter sweeps
- ✅ Fairness analysis

**Time:** ~30 minutes
**Level:** Beginner to Intermediate

**Quick Start:**
```bash
# From package root
cd notebooks
jupyter notebook agorai_demo.ipynb
```

## Prerequisites

### Installation

```bash
# Install package with research features
pip install -e ..[research]

# Or from PyPI (once published)
pip install agorai[research]

# Install Jupyter
pip install jupyter pandas matplotlib
```

### Python Packages Required

- `agorai[research]` - The main package with benchmarking + visualization
- `jupyter` - Jupyter notebook environment
- `pandas` - For data display (optional)
- `matplotlib` - For plotting (required for visualization)
- `numpy` - For numerical operations (included with matplotlib)

## Running the Notebooks

### Option 1: Jupyter Notebook

```bash
# From notebooks/ directory
jupyter notebook

# Then open agorai_demo.ipynb in your browser
```

### Option 2: JupyterLab

```bash
# Install JupyterLab
pip install jupyterlab

# Launch
jupyter lab

# Open agorai_demo.ipynb
```

### Option 3: VS Code

1. Open VS Code
2. Install "Jupyter" extension
3. Open `agorai_demo.ipynb`
4. Select Python kernel
5. Run cells with Shift+Enter

## Notebook Contents

### Part 1: Core Aggregation
- Define utility matrices
- Try different aggregation methods
- Compare results across methods

### Part 2: Benchmarking
- Use built-in benchmarks
- Evaluate single methods
- Compare multiple methods scientifically

### Part 3: Visualization
- Plot utility heatmaps
- Create method comparison charts
- Visualize fairness-efficiency tradeoffs

### Part 4: Natural Language Explanations
- Explain specific decisions
- Understand how methods work
- Compare explanations across methods

### Part 5: Advanced Example
- Parameter sweep (Atkinson epsilon)
- Visualize fairness-efficiency relationship
- Interpret tradeoffs

### Part 6: Real-World Scenario
- Content moderation use case
- Multiple cultural perspectives
- Fairness analysis
- Recommended decision

## Expected Outputs

When you run the demo notebook, it will generate:

**Plots:**
- `utility_heatmap.png` - Utility matrix visualization
- `method_comparison.png` - Side-by-side method comparison
- `fairness_efficiency_tradeoff.png` - Scatter plot of tradeoffs
- `parameter_sweep.png` - Epsilon parameter sweep results
- `content_moderation_utilities.png` - Real-world scenario visualization

**Data:**
- `comparison_results.json` - Method comparison results

**Console Output:**
- Aggregation results for each method
- Benchmark metrics (fairness, efficiency, agreement)
- Natural language explanations
- Fairness analysis tables

## Customization

### Using Your Own Data

Replace the utility matrix with your own:

```python
# Your custom utility matrix
my_utilities = [
    [0.9, 0.3, 0.5],  # Agent 1 utilities
    [0.2, 0.8, 0.6],  # Agent 2 utilities
    # ... more agents
]

# Run aggregation
result = aggregate(my_utilities, method="atkinson", epsilon=1.0)
```

### Creating Custom Benchmarks

```python
from agorai.benchmarks import register_benchmark

my_benchmark = {
    'name': 'my_custom_benchmark',
    'description': 'Description here',
    'items': [
        {'utilities': [[0.8, 0.2], [0.3, 0.7]], 'ground_truth': 0},
        # ... more test cases
    ]
}

register_benchmark("my_custom_benchmark", my_benchmark)

# Use it
results = evaluate_method("atkinson", "my_custom_benchmark")
```

### Trying Different Methods

All available methods:
```python
from agorai.aggregate import list_methods

methods = list_methods()
print(methods)
# ['majority', 'weighted_plurality', 'borda', 'schulze_condorcet',
#  'approval_voting', 'supermajority', 'maximin', 'atkinson',
#  'nash_bargaining', 'score_centroid', 'robust_median', 'consensus',
#  'quadratic_voting', 'veto_hybrid']
```

## Troubleshooting

### Import Errors

```python
# If you get "ModuleNotFoundError: No module named 'agorai'"
import sys
sys.path.insert(0, '../src')  # Add package to path
```

Or install the package:
```bash
pip install -e ..[research]
```

### Plotting Not Working

```python
# If plots don't show, ensure matplotlib is installed
pip install matplotlib

# Set inline backend for Jupyter
%matplotlib inline
```

### Performance Issues

If evaluation is slow:
- Reduce number of test cases in benchmarks
- Use fewer methods in comparisons
- Decrease parameter sweep resolution

## Next Steps

After completing the demo notebook:

1. **Read Documentation**
   - [Aggregation API](../docs/aggregate.md)
   - [Benchmarking Guide](../docs/benchmarks.md)
   - [Visualization Guide](../docs/visualization.md)

2. **Try Your Own Use Cases**
   - Modify the notebook for your data
   - Create custom benchmarks
   - Experiment with parameters

3. **Explore Research**
   - Read [Research Strategy Report](../../AgorAI_Research_Strategy_Report.md)
   - Check [AI Research Report](../../AI_Research_2024_2025_Comprehensive_Report.md)
   - Explore connections to your research

4. **Contribute**
   - Create new notebooks for specific use cases
   - Share your benchmarks
   - Report bugs or suggest features

## Contributing Notebooks

We welcome contributions of notebooks demonstrating:

- Specific use cases (healthcare, finance, education)
- Integration with other libraries (LangChain, HuggingFace)
- Advanced techniques (MARL, Constitutional AI)
- Comparative studies with other methods

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

## Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/agorai/issues)
- **Questions**: [GitHub Discussions](https://github.com/yourusername/agorai/discussions)
- **Email**: samuel.schlenker@example.com

---

**Happy exploring! 🚀**
