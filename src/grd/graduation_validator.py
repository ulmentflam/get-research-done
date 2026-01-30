"""Graduation validation module for GRD notebooks.

This module validates that notebooks meet graduation requirements before
converting to production scripts. It implements a tiered validation approach:
- Hard requirements (errors): Block graduation, must be fixed
- Advisory warnings: Logged but don't block graduation

Per CONTEXT.md:
- Reproducibility checks block graduation (random seeds, parameters cell)
- Style checks warn only (hardcoded paths, magic commands)
"""
import re
from pathlib import Path
from typing import Any

import nbformat


def validate_graduation_requirements(notebook_path: str) -> dict[str, Any]:
    """
    Validate notebook against graduation checklist.

    Checks notebook for graduation requirements before conversion to
    production script. Uses tiered validation:

    Hard requirements (errors - block graduation):
        - Random seed must be explicitly set (numpy, torch, random, etc.)
        - Must have cell tagged with 'parameters' for parameterization

    Advisory warnings (don't block graduation):
        - Hardcoded absolute paths (will break across environments)
        - Magic commands (will cause SyntaxError in .py files)
        - Shell commands (will break in non-notebook execution)

    Args:
        notebook_path: Path to the notebook file to validate

    Returns:
        Dict with keys:
            - passed: bool - True if all hard requirements met (no errors)
            - errors: list[str] - Blocking issues that prevent graduation
            - warnings: list[str] - Advisory issues (logged but don't block)

    Example:
        >>> validation = validate_graduation_requirements(
        ...     "notebooks/exploration/experiment.ipynb"
        ... )
        >>> if not validation['passed']:
        ...     print("GRADUATION BLOCKED:")
        ...     for error in validation['errors']:
        ...         print(f"  - {error}")
        >>> if validation['warnings']:
        ...     print("WARNINGS (advisory):")
        ...     for warning in validation['warnings']:
        ...         print(f"  - {warning}")
    """
    nb = nbformat.read(notebook_path, as_version=4)
    errors: list[str] = []
    warnings: list[str] = []

    # === HARD REQUIREMENTS (errors block graduation) ===

    # Hard requirement 1: Random seed must be explicitly set
    has_random_seed = _check_random_seed(nb)
    if not has_random_seed:
        errors.append(
            "Random seed not explicitly set. Must set at least one of: "
            "random.seed(), np.random.seed(), torch.manual_seed(), or random_seed = <value>"
        )

    # Hard requirement 2: Must have parameters cell tag
    has_parameters_cell = _check_parameters_cell(nb)
    if not has_parameters_cell:
        errors.append(
            "No cell tagged with 'parameters'. "
            "Papermill requires a cell with the 'parameters' tag for parameter injection."
        )

    # === ADVISORY WARNINGS (don't block graduation) ===

    # Advisory 1: Warn on hardcoded absolute paths
    path_warnings = _check_hardcoded_paths(nb)
    warnings.extend(path_warnings)

    # Advisory 2: Warn on magic commands (will break in script)
    magic_warnings = _check_magic_commands(nb)
    warnings.extend(magic_warnings)

    # Advisory 3: Warn on shell commands (will break in script)
    shell_warnings = _check_shell_commands(nb)
    warnings.extend(shell_warnings)

    return {
        'passed': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }


def _check_random_seed(nb: nbformat.NotebookNode) -> bool:
    """Check if random seed is explicitly set anywhere in the notebook."""
    seed_patterns = [
        r'random\.seed\s*\(',           # random.seed(42)
        r'np\.random\.seed\s*\(',       # np.random.seed(42)
        r'numpy\.random\.seed\s*\(',    # numpy.random.seed(42)
        r'torch\.manual_seed\s*\(',     # torch.manual_seed(42)
        r'tf\.random\.set_seed\s*\(',   # tf.random.set_seed(42)
        r'random_seed\s*=',             # random_seed = 42 (parameter pattern)
        r'seed\s*=\s*\d+',              # seed=42 as keyword arg
    ]

    for cell in nb.cells:
        if cell.cell_type == 'code':
            for pattern in seed_patterns:
                if re.search(pattern, cell.source):
                    return True
    return False


def _check_parameters_cell(nb: nbformat.NotebookNode) -> bool:
    """Check if any cell has the 'parameters' tag."""
    for cell in nb.cells:
        tags = cell.metadata.get('tags', [])
        if 'parameters' in tags:
            return True
    return False


def _check_hardcoded_paths(nb: nbformat.NotebookNode) -> list[str]:
    """Check for hardcoded absolute paths that will break across environments."""
    warnings = []

    # Patterns for common hardcoded paths
    path_patterns = [
        (r'["\']\/Users\/[^"\']+["\']', '/Users/'),
        (r'["\']\/home\/[^"\']+["\']', '/home/'),
        (r'["\'][A-Za-z]:\\\\[^"\']+["\']', 'Windows drive path'),
        (r'["\']~\/[^"\']+["\']', '~/'),
    ]

    for cell_idx, cell in enumerate(nb.cells):
        if cell.cell_type == 'code':
            for pattern, description in path_patterns:
                matches = re.findall(pattern, cell.source)
                for match in matches:
                    # Truncate long paths for readability
                    truncated = match[:60] + '...' if len(match) > 60 else match
                    warnings.append(
                        f"Hardcoded {description} path in cell {cell_idx}: {truncated} "
                        "(use relative paths or parameters)"
                    )

    return warnings


def _check_magic_commands(nb: nbformat.NotebookNode) -> list[str]:
    """Check for IPython magic commands that will break in Python scripts."""
    warnings = []

    # Pattern for magic commands at start of line
    # Matches %command or %%command but not strings containing %
    magic_pattern = r'^[%]{1,2}\w+'

    for cell_idx, cell in enumerate(nb.cells):
        if cell.cell_type == 'code':
            for line in cell.source.split('\n'):
                stripped = line.strip()
                if re.match(magic_pattern, stripped):
                    # Truncate long commands
                    truncated = stripped[:50] + '...' if len(stripped) > 50 else stripped
                    warnings.append(
                        f"Magic command in cell {cell_idx}: {truncated} "
                        "(remove or convert before graduation)"
                    )

    return warnings


def _check_shell_commands(nb: nbformat.NotebookNode) -> list[str]:
    """Check for shell commands (! prefix) that will break in Python scripts."""
    warnings = []

    # Pattern for shell commands at start of line
    shell_pattern = r'^!\s*\w+'

    for cell_idx, cell in enumerate(nb.cells):
        if cell.cell_type == 'code':
            for line in cell.source.split('\n'):
                stripped = line.strip()
                if re.match(shell_pattern, stripped):
                    # Truncate long commands
                    truncated = stripped[:50] + '...' if len(stripped) > 50 else stripped
                    warnings.append(
                        f"Shell command in cell {cell_idx}: {truncated} "
                        "(move to requirements.txt or script)"
                    )

    return warnings
