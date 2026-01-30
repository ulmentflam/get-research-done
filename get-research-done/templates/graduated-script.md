# Graduated Script Template

This template is used when graduating an exploration notebook to a validated Python script via `/grd:graduate`.

## Template Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `{{experiment_name}}` | OBJECTIVE.md or notebook filename | Human-readable experiment name |
| `{{source_notebook}}` | User input | Path to source notebook (e.g., `notebooks/exploration/001_initial.ipynb`) |
| `{{source_run}}` | Run directory | Run that achieved PROCEED verdict (e.g., `experiments/run_003_baseline`) |
| `{{critic_verdict}}` | CRITIC.md | Critic verdict (always PROCEED for graduation) |
| `{{verdict_date}}` | CRITIC.md | ISO 8601 date of verdict |
| `{{graduation_timestamp}}` | System | ISO 8601 timestamp when graduated |

## Python Script Template

```python
"""
Validated experiment: {{experiment_name}}

Source notebook: {{source_notebook}}
Source run: {{source_run}}
Critic verdict: {{critic_verdict}} ({{verdict_date}})
Graduated: {{graduation_timestamp}}

MANUAL REFACTORING REQUIRED:
- [ ] Remove/convert magic commands (grep "^%")
- [ ] Extract code into functions
- [ ] Replace parameter cell with argparse
- [ ] Add docstrings and type hints
- [ ] Set all random seeds explicitly
- [ ] Write tests for core functions

This script was auto-generated from a validated notebook.
Review and complete the refactoring checklist above before production use.
"""

import argparse
import random
from typing import Any

import numpy as np

# Uncomment if using PyTorch:
# import torch

# Uncomment if using TensorFlow:
# import tensorflow as tf


def set_random_seeds(seed: int = 42) -> None:
    """Set all random seeds for reproducibility.

    Args:
        seed: Random seed value (default: 42)
    """
    random.seed(seed)
    np.random.seed(seed)

    # Uncomment for PyTorch:
    # torch.manual_seed(seed)
    # torch.cuda.manual_seed_all(seed)
    # torch.backends.cudnn.deterministic = True
    # torch.backends.cudnn.benchmark = False

    # Uncomment for TensorFlow:
    # tf.random.set_seed(seed)


def main(args: argparse.Namespace) -> dict[str, Any]:
    """Main experiment entry point.

    Args:
        args: Parsed command line arguments

    Returns:
        Dictionary containing experiment results/metrics
    """
    set_random_seeds(args.random_seed)

    # ---------------------------------------------------------------------
    # TODO: Implement experiment logic here
    # Extracted from: {{source_notebook}}
    #
    # Refactoring guidance:
    # 1. Convert notebook cells to functions
    # 2. Add type hints to all function signatures
    # 3. Replace hardcoded values with args.* parameters
    # 4. Return metrics as a dictionary for logging
    # ---------------------------------------------------------------------

    results = {
        "status": "not_implemented",
        "message": "Replace this with actual experiment implementation"
    }

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="{{experiment_name}}",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Standard arguments
    parser.add_argument(
        "--random-seed",
        type=int,
        default=42,
        help="Random seed for reproducibility"
    )

    # TODO: Add experiment-specific arguments
    # Example:
    # parser.add_argument("--learning-rate", type=float, default=0.001)
    # parser.add_argument("--epochs", type=int, default=100)
    # parser.add_argument("--batch-size", type=int, default=32)
    # parser.add_argument("--data-path", type=str, required=True)

    args = parser.parse_args()

    results = main(args)
    print(f"Experiment complete: {results}")
```

## Usage

The graduation workflow:

1. **Notebook achieves PROCEED verdict** via `/grd:research`
2. **User initiates graduation** via `/grd:graduate`
3. **System converts notebook to script** using nbconvert
4. **System prepends this header template** with filled variables
5. **Script lands in** `src/experiments/{{sanitized_experiment_name}}.py`
6. **User completes refactoring checklist** before production use

## Refactoring Checklist Details

### Remove/convert magic commands
```bash
# Find magic commands in the generated script
grep "^%" src/experiments/your_script.py
```
Common conversions:
- `%matplotlib inline` - Remove (not needed in scripts)
- `%load_ext autoreload` - Remove (not applicable)
- `%%time` - Replace with `time.time()` or profiling
- `!pip install` - Move to requirements.txt

### Extract code into functions
- Each logical block should be a function
- Functions should have single responsibility
- Return values instead of relying on globals

### Replace parameter cell with argparse
- Identify cells tagged 'parameters' or variable definitions
- Convert each parameter to `parser.add_argument()`
- Use type hints and defaults from original values

### Add docstrings and type hints
- Every function needs a docstring
- Use Google or NumPy docstring style consistently
- Add type hints to all arguments and return values

### Set all random seeds explicitly
- Call `set_random_seeds()` at start of `main()`
- Pass seed through all library calls that accept it
- Document any randomness that cannot be seeded

### Write tests for core functions
- Create `tests/test_{{sanitized_experiment_name}}.py`
- Test pure functions with known inputs/outputs
- Test edge cases and error conditions

---

*Template version: 1.0*
*Phase: 06-notebook-support*
