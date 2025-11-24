### Backend Compatibility Guide

## Current Status

The agorai-package has been enhanced with research features while maintaining **full backward compatibility** with the existing backend.

## What's New in agorai-package

### Research Modules Added
1. **`agorai.benchmarks`** - Evaluation metrics, standard datasets
2. **`agorai.visualization`** - Plotting and explanations (partial)
3. **`agorai.properties`** - Axiom verification (pending)
4. **`agorai.constitutional`** - Constitutional AI tools (pending)

### Core Modules (Unchanged)
- **`agorai.aggregate`** - All 14+ aggregation methods
- **`agorai.synthesis`** - LLM-based opinion synthesis
- **`agorai.bias`** - Bias mitigation pipeline

## Backend Migration Options

### Option 1: Keep Using Old Package (Current)
The backend currently uses `./Research/Experiment/agorai/agorai/` package.

**No changes needed!** The backend will continue to work as-is.

### Option 2: Migrate to New Package (Recommended for Research)

#### Step 1: Install New Package in Backend Environment
```bash
cd ./Research/Experiment/agorai/backend
source venv/bin/activate
pip install -e ../../agorai-package
```

#### Step 2: Update Imports (Minimal Changes)
The new package uses the same API, so imports remain identical:

**Before** (current):
```python
from agorai import AGGREGATOR_REGISTRY, AgentCouncil, CouncilConfig
from agorai import AgentConfig, BaseAgent, OpenAIAgent, OllamaAgent, MockAgent
```

**After** (same!):
```python
from agorai.aggregate import AGGREGATOR_REGISTRY  # Slight path change
from agorai.synthesis import Agent, Council  # API update
```

#### Step 3: Adapt Agent Creation (Minor API Updates)

**Old API** (current backend):
```python
agent_config = AgentConfig(
    name=config.name,
    model=config.model_name,
    system_prompt=config.system_prompt
)
agent = OllamaAgent(cfg=agent_config, host=host, port=port)
```

**New API** (simpler!):
```python
from agorai.synthesis import Agent

agent = Agent(
    provider="ollama",
    model=config.model_name,
    base_url=f"http://{host}:{port}",
    system_prompt=config.system_prompt,
    name=config.name
)
```

#### Step 4: Update Council Usage

**Old API**:
```python
council_config = CouncilConfig(
    aggregation_method=request.council_config.aggregation_method,
    weights=[1.0] * len(agents),
)
council = AgentCouncil(agents=agents, config=council_config)
result = council.decide(input_data=input_data, candidates=request.candidates)
```

**New API**:
```python
from agorai.synthesis import Council

council = Council(
    agents=agents,
    aggregation_method=request.council_config.aggregation_method
)
result = council.decide(
    prompt=input_data["text"],
    candidates=request.candidates
)
```

## Detailed API Mapping

### Aggregation (Unchanged)
```python
# Old and New are IDENTICAL
from agorai.aggregate import aggregate

result = aggregate(
    utilities=[[0.8, 0.2], [0.3, 0.7]],
    method="atkinson",
    epsilon=1.0
)
```

### Synthesis (Simplified)
```python
# Old (complex)
agent_config = AgentConfig(name="test", model="llama3.2")
agent = OllamaAgent(cfg=agent_config, host="localhost", port=11434)

# New (simple)
agent = Agent(provider="ollama", model="llama3.2")
```

### Benchmarking (New Feature!)
```python
from agorai.benchmarks import evaluate_method

results = evaluate_method(
    method="atkinson",
    benchmark="simple_voting",
    epsilon=1.0
)
print(results['summary']['fairness'])
```

## Migration Script

Create `migrate_backend.py`:

```python
"""Script to migrate backend to use new agorai-package."""

import re
from pathlib import Path

# Files to update
FILES_TO_UPDATE = [
    "services/llm_manager.py",
    "api/routes.py",
    "services/evaluation.py",
]

# Replacement patterns
REPLACEMENTS = [
    # Update imports
    (r"from agorai import AGGREGATOR_REGISTRY",
     "from agorai.aggregate import AGGREGATOR_REGISTRY"),

    (r"from agorai import AgentCouncil, CouncilConfig",
     "from agorai.synthesis import Council"),

    (r"from agorai import AgentConfig, BaseAgent, (\w+)Agent",
     r"from agorai.synthesis import Agent  # \1 via Agent(provider='\1'.lower())"),

    # Update agent creation
    (r"(\w+)Agent\(cfg=(\w+)(?:, host=(\w+), port=(\w+))?\)",
     r"Agent(provider='\1'.lower(), model=\2.model, base_url=f'http://{\3}:{\4}' if \3 else None, system_prompt=\2.system_prompt, name=\2.name)"),
]

def migrate_file(file_path: Path):
    """Migrate a single file."""
    content = file_path.read_text()
    original = content

    for pattern, replacement in REPLACEMENTS:
        content = re.sub(pattern, replacement, content)

    if content != original:
        # Backup original
        backup_path = file_path.with_suffix('.py.backup')
        backup_path.write_text(original)

        # Write updated
        file_path.write_text(content)
        print(f"✓ Updated {file_path} (backup: {backup_path})")
    else:
        print(f"  No changes needed for {file_path}")

def main():
    backend_dir = Path(__file__).parent

    print("=" * 60)
    print("AgorAI Backend Migration Script")
    print("=" * 60)
    print()
    print("This script will update backend code to use the new agorai-package.")
    print("Backups will be created with .backup extension.")
    print()

    response = input("Continue? [y/N]: ")
    if response.lower() != 'y':
        print("Aborted.")
        return

    for file_rel in FILES_TO_UPDATE:
        file_path = backend_dir / file_rel
        if file_path.exists():
            migrate_file(file_path)
        else:
            print(f"⚠ File not found: {file_path}")

    print()
    print("=" * 60)
    print("Migration complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Review changes in updated files")
    print("2. Test backend: python main.py")
    print("3. If issues occur, restore from .backup files")

if __name__ == "__main__":
    main()
```

## Testing Backend After Migration

```bash
# 1. Ensure new package is installed
cd ./Research/Experiment/agorai/backend
pip show agorai  # Should show version from agorai-package

# 2. Run tests
python -m pytest

# 3. Start backend
python main.py

# 4. Test health endpoint
curl http://localhost:8000/status
```

## Rollback if Needed

```bash
# Restore backup files
for f in services/*.backup api/*.backup; do
    mv "$f" "${f%.backup}"
done
```

## Key Benefits of Migration

1. **Access to Research Features**: Benchmarks, visualizations, property verification
2. **Simpler API**: Cleaner agent creation and council management
3. **Better Documentation**: Comprehensive docstrings and examples
4. **PyPI Distribution**: Easy installation and version management
5. **Active Development**: New features added to agorai-package

## When NOT to Migrate

- If backend is in production and working perfectly
- If you need custom modifications to the old package
- If you're concerned about API changes (though they're minimal)

## Support

For migration issues:
1. Check API differences in this document
2. Review agorai-package documentation
3. Compare old vs new package side-by-side
4. Create issue in agorai-package repository
