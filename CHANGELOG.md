# Changelog

All notable changes to AgorAI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-11-21

### Added - Research Modules ✨

#### Queue Processing Module (`agorai.queue`)
- **Core Functions**:
  - `load_requests_from_file()` - Load aggregation requests from JSON files
  - `process_single_request()` - Process one aggregation request
  - `process_queue()` - Process multiple requests from a file
  - `compare_methods_on_queue()` - Compare methods on the same request queue

- **Metrics** (3 categories, 10 total metrics):
  - **Fairness**: Gini coefficient, Atkinson index, variance, coefficient of variation
  - **Efficiency**: Social welfare, utilitarian welfare, Pareto efficiency
  - **Agreement**: Consensus score, average support, minimum support

- **Use Cases**:
  - Production batch processing (daily decisions, content moderation, etc.)
  - Testing on datasets (benchmarks, test cases)
  - Evaluating multiple scenarios
  - Method comparison across many cases

- **Features**:
  - File-based request queues (JSON format)
  - Scientific evaluation with rigorous metrics
  - Optional ground truth for accuracy calculation
  - Per-item and aggregate statistics
  - Method rankings

#### Visualization Module (`agorai.visualization`)
- **Plotting Functions** (requires matplotlib):
  - `plot_utility_matrix()` - Heatmap visualization of utilities
  - `plot_aggregation_comparison()` - Side-by-side method comparison
  - `plot_fairness_tradeoffs()` - Fairness vs efficiency scatter plots

- **Explanation Functions**:
  - `explain_decision()` - Natural language explanation of aggregation decisions
  - `explain_method()` - Method documentation (properties, when to use, etc.)

- **Supported Methods** (detailed explanations):
  - Majority, Atkinson, Maximin, Borda, Centroid, Nash Bargaining
  - Generic fallback for other methods

- **Features**:
  - Publication-quality plots (PNG/PDF export)
  - Markdown-formatted explanations
  - Interpretable AI decisions
  - Customizable labels and colors

#### Package Utilities
- `has_queue()` - Check if queue module available
- `has_visualization()` - Check if visualization module available
- Optional dependencies for research features

### Changed

- **Version**: Bumped to 0.2.0 (semantic versioning)
- **Documentation**:
  - Updated README with research features
  - Added badges (PyPI version, Python version, license)
  - Reorganized sections with emojis for clarity
  - Added "Research & Papers" section
  - Expanded use cases with research applications
  - Added roadmap (v0.3.0, v0.4.0)
  - Added acknowledgments section

- **Installation**:
  - New `[research]` extra for queue processing + visualization
  - Updated `[all]` to include research features

### Documentation

- **New Guides**:
  - `docs/queue.md` - Complete queue processing guide (30+ pages)
  - `docs/visualization.md` - Complete visualization guide (20+ pages)
  - `BACKEND_COMPATIBILITY.md` - Migration guide for existing backends
  - `PACKAGE_ENHANCEMENTS_SUMMARY.md` - Implementation summary

- **Enhanced README**:
  - Added 2 new quick start examples (queue processing, visualization)
  - Expanded aggregation methods table
  - Added research connections (EBMs, Constitutional AI, o1, MARL)
  - Added citation template (BibTeX)
  - Added contributing guidelines
  - Added contact information

### Infrastructure

- **Module Structure**:
  ```
  src/agorai/
  ├── aggregate/       (existing)
  ├── synthesis/       (existing)
  ├── bias/            (existing)
  ├── queue/           ✨ NEW
  │   ├── core.py      (queue processing framework)
  │   └── metrics.py   (fairness/efficiency/agreement)
  └── visualization/   ✨ NEW
      ├── plots.py     (plotting utilities)
      └── explanations.py (NL explanations)
  ```

- **Code Quality**:
  - ~1,900 lines of new, documented code
  - Comprehensive docstrings with examples
  - Type hints throughout
  - Modular, extensible design

### Performance

- Queue processing: Evaluates methods in <100ms per request for typical cases
- Visualization: Generates plots in <1s
- No performance impact on core aggregation (modular design)

### Compatibility

- **Backward Compatible**: All existing code continues to work
- **Python**: 3.8+ (unchanged)
- **Optional Dependencies**:
  - matplotlib (for plotting): `pip install agorai[research]`
  - No new required dependencies for core features

### Known Issues

- Property verification module not yet implemented (planned for v0.3.0)
- Constitutional module not yet implemented (planned for v0.4.0)
- Built-in example dataset (`SIMPLE_VOTING_EXAMPLE`) is minimal - users should provide their own request files
- Visualization requires matplotlib (optional dependency)

---

## [0.1.0] - 2024-11-20

### Added

#### Core Aggregation Module (`agorai.aggregate`)
- 14+ aggregation methods from social choice theory, welfare economics, game theory:
  - **Social Choice**: majority, weighted_plurality, borda, schulze_condorcet, approval_voting, supermajority
  - **Welfare Economics**: maximin, atkinson, nash_bargaining
  - **Machine Learning**: score_centroid, robust_median, consensus
  - **Game Theory**: quadratic_voting, veto_hybrid

- Core Functions:
  - `aggregate()` - Main aggregation function
  - `list_methods()` - List available methods
  - Registry system for extensibility

#### Synthesis Module (`agorai.synthesis`)
- Multi-provider LLM integration:
  - OpenAI (GPT-4, GPT-4 Turbo, GPT-4o, etc.)
  - Anthropic (Claude 3.5 Sonnet, Opus, Haiku)
  - Ollama (Llama 3.2, Mistral, Mixtral, Gemma 2, etc.)
  - Google (Gemini models)

- Features:
  - Unified agent interface across providers
  - Democratic opinion synthesis
  - Multimodal support (text + images)
  - Streaming responses

#### Bias Mitigation Module (`agorai.bias`)
- Full pipeline for bias detection and mitigation
- Cultural perspective diversity
- Configurable contexts and aggregation methods

#### Documentation
- Complete API reference (`docs/aggregate.md`)
- Quick start guide (`QUICK_START.md`)
- PyPI upload guide (`PYPI_UPLOAD_GUIDE.md`)
- Migration guide (`BACKEND_MIGRATION_GUIDE.md`)
- Project summary (`PROJECT_SUMMARY.md`)

#### Examples
- Basic usage examples
- Backend integration examples
- Jupyter notebooks

### Infrastructure

- Package structure with setuptools
- Poetry for dependency management
- pytest for testing
- Pre-commit hooks
- GitHub Actions CI/CD (planned)

### License

- Custom Research and Non-Commercial License
- Free for academic research, education, personal use
- Commercial use requires agreement

---

## [Unreleased] - Future Versions

### Planned for v0.3.0
- [ ] Property verification module (`agorai.properties`)
  - Formal axiom verification (anonymity, monotonicity, Pareto, IIA, etc.)
  - Strategyproofness testing
  - Computational complexity analysis

- [ ] Additional example datasets
  - PRISM dataset (cross-cultural preferences, 1,500 people, 75 countries)
  - Social choice voting datasets from literature
  - Constitutional preferences simulations

- [ ] Interactive visualizations
  - Plotly-based dashboards
  - Real-time method comparison
  - Parameter sweep animations

- [ ] Framework integrations
  - LangChain integration
  - HuggingFace Transformers integration
  - AutoGen integration
  - OpenAI Swarm integration

### Planned for v0.4.0
- [ ] Constitutional AI module (`agorai.constitutional`)
  - Democratic constitution design tools
  - Multi-principle aggregation
  - Constitutional council management
  - Integration with Anthropic's CCAI

- [ ] MARL integration (`agorai.rl`)
  - Democratic reward aggregation
  - Multi-agent RL environments
  - Fairness-aware training

- [ ] Federated learning
  - Democratic model aggregation
  - Privacy-preserving aggregation
  - Robust aggregation against attacks

- [ ] Advanced metrics
  - Shapley values for agent contribution
  - Causal analysis of decisions
  - Uncertainty quantification

### Planned for v0.5.0
- [ ] Web interface
  - Interactive demo
  - Method comparison tool
  - Constitutional design interface

- [ ] Deployment tools
  - Docker containers
  - Cloud deployment (AWS, GCP, Azure)
  - REST API server

- [ ] Performance optimizations
  - Cython extensions for core algorithms
  - GPU acceleration for large-scale aggregation
  - Distributed computing support

---

## Version History

- **0.2.0** (2025-11-21): Research modules added (queue processing, visualization)
- **0.1.0** (2024-11-20): Initial release (aggregation, synthesis, bias mitigation)

---

## Notes

### Semantic Versioning

- **MAJOR** (X.0.0): Incompatible API changes
- **MINOR** (0.X.0): New features (backward compatible)
- **PATCH** (0.0.X): Bug fixes (backward compatible)

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute to AgorAI.

### Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/agorai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/agorai/discussions)
- **Email**: samuel.schlenker@example.com

---

**Thank you to all contributors who made these releases possible!**
