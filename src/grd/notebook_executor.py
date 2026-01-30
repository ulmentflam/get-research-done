"""Notebook execution module for GRD experiments.

This module provides the core execution engine for running Jupyter notebooks
through the GRD validation loop with full reproducibility guarantees:
- Fresh kernel per run (papermill handles automatically)
- Cell-level timeouts to catch infinite loops
- Structured output extraction via scrapbook
- Retry logic for transient failures
"""
import json
import time
from pathlib import Path
from typing import Any

import papermill as pm
import scrapbook as sb


def execute_notebook_experiment(
    notebook_path: str,
    run_dir: Path,
    parameters: dict[str, Any],
    execution_timeout: int = 300,
    start_timeout: int = 60,
    retry_on_failure: bool = True
) -> dict[str, Any]:
    """
    Execute a notebook as a GRD experiment with reproducibility guarantees.

    This function executes a parameterized Jupyter notebook using papermill,
    extracts metrics via scrapbook, and saves results to the run directory.
    Each execution uses a fresh kernel to ensure reproducibility.

    Args:
        notebook_path: Path to input notebook (e.g., "notebooks/exploration/exp.ipynb")
        run_dir: Directory for outputs (e.g., Path("experiments/run_042"))
        parameters: Dict of parameters to inject. MUST include 'random_seed' key
            for reproducibility validation.
        execution_timeout: Seconds per cell before timeout (default: 300 = 5 min).
            Applies to each cell individually, not total execution.
        start_timeout: Seconds to wait for kernel startup (default: 60).
        retry_on_failure: If True, retry once on execution failure before
            marking run as failed (default: True).

    Returns:
        Dict with keys:
            - success: bool - True if notebook executed without errors
            - output_notebook: str | None - Path to executed notebook with outputs
            - metrics: dict - All metrics extracted via scrapbook glue()
            - error: str | None - Error message if execution failed
            - execution_time_seconds: float - Total execution time

    Raises:
        ValueError: If 'random_seed' not in parameters (hard requirement for
            reproducibility per GRD graduation requirements).

    Example:
        >>> result = execute_notebook_experiment(
        ...     notebook_path="notebooks/exploration/001_initial_test.ipynb",
        ...     run_dir=Path("experiments/run_042"),
        ...     parameters={
        ...         'alpha': 0.6,
        ...         'learning_rate': 0.001,
        ...         'random_seed': 42,
        ...         'data_path': 'data/train.csv'
        ...     }
        ... )
        >>> if result['success']:
        ...     print(f"Metrics: {result['metrics']}")
    """
    start_time = time.time()

    # Validate random seed exists (hard requirement per CONTEXT.md)
    if 'random_seed' not in parameters:
        raise ValueError(
            "parameters must include 'random_seed' for reproducibility. "
            "GRD requires explicit random seed management to ensure reproducible results."
        )

    # Ensure run directory exists
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    output_path = run_dir / "output.ipynb"

    # Determine retry attempts
    max_attempts = 2 if retry_on_failure else 1
    attempt = 0
    last_error = None

    while attempt < max_attempts:
        attempt += 1
        try:
            # Execute with papermill (fresh kernel per run - automatic)
            # kernel_name=None auto-detects from notebook metadata,
            # falls back to current environment if not specified
            pm.execute_notebook(
                notebook_path,
                str(output_path),
                parameters=parameters,
                execution_timeout=execution_timeout,
                start_timeout=start_timeout,
                kernel_name=None,  # Auto-detect from notebook metadata
            )

            # Extract metrics with scrapbook
            nb = sb.read_notebook(str(output_path))
            metrics = {
                name: scrap.data
                for name, scrap in nb.scraps.items()
            }

            # Add execution time to metrics
            execution_time = time.time() - start_time
            metrics['execution_time_seconds'] = execution_time

            # Save metrics to JSON file
            metrics_path = run_dir / "metrics.json"
            with open(metrics_path, 'w') as f:
                json.dump(metrics, f, indent=2, default=str)

            return {
                'success': True,
                'output_notebook': str(output_path),
                'metrics': metrics,
                'error': None,
                'execution_time_seconds': execution_time
            }

        except pm.PapermillExecutionError as e:
            last_error = str(e)
            if attempt < max_attempts:
                print(f"Execution failed (attempt {attempt}/{max_attempts}): {e}")
                print("Retrying...")
            # Continue to next attempt or exit loop

    # All attempts failed
    execution_time = time.time() - start_time

    # Try to extract partial metrics if output notebook exists
    metrics = {}
    output_notebook_path = None
    if output_path.exists():
        output_notebook_path = str(output_path)
        try:
            nb = sb.read_notebook(str(output_path))
            metrics = {
                name: scrap.data
                for name, scrap in nb.scraps.items()
            }
        except Exception:
            # Failed to extract metrics from partial notebook
            pass

    metrics['execution_time_seconds'] = execution_time

    # Save whatever metrics we have (even if empty, for consistency)
    metrics_path = run_dir / "metrics.json"
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2, default=str)

    return {
        'success': False,
        'output_notebook': output_notebook_path,
        'metrics': metrics,
        'error': last_error,
        'execution_time_seconds': execution_time
    }
