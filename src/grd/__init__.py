"""GRD Python utilities for notebook execution, graduation validation, and data exploration."""

# Lazy imports to avoid dependency issues when only using hardware module
__all__ = [
    'execute_notebook_experiment',
    'validate_graduation_requirements',
    'quick_explore',
    'generate_insights',
]


def __getattr__(name):
    """Lazy import to avoid loading all modules at package import time."""
    if name == "execute_notebook_experiment":
        from .notebook_executor import execute_notebook_experiment
        return execute_notebook_experiment
    elif name == "validate_graduation_requirements":
        from .graduation_validator import validate_graduation_requirements
        return validate_graduation_requirements
    elif name == "quick_explore":
        from .quick import quick_explore
        return quick_explore
    elif name == "generate_insights":
        from .insights import generate_insights
        return generate_insights
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
