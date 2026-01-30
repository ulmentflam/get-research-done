"""Duration estimation for ML experiments based on hardware context."""

import logging
from typing import TypedDict

logger = logging.getLogger(__name__)


class DurationEstimate(TypedDict):
    """Duration estimate for an experiment."""
    estimated_seconds: float
    estimated_minutes: float
    estimated_hours: float
    is_long_running: bool
    requires_user_confirmation: bool
    gpu_tflops: float
    confidence: str


def estimate_training_duration(
    num_samples: int,
    num_epochs: int,
    model_params: int,
    hardware_profile: dict,
    batch_size: int = 32,
) -> DurationEstimate:
    """
    Estimate training time based on hardware specs and data size.

    Uses GPU TFLOPs lookup table for common GPUs, computes total FLOPs
    required (6 * params * samples * epochs for forward + backward pass),
    and applies 50% efficiency factor for realistic estimates.

    Long-running threshold: 600 seconds (10 minutes)

    Args:
        num_samples: Number of training samples
        num_epochs: Number of training epochs
        model_params: Number of model parameters
        hardware_profile: Hardware profile from capture_hardware_profile()
        batch_size: Batch size (default: 32)

    Returns:
        DurationEstimate with time estimates, is_long_running flag, and confidence

    Examples:
        >>> profile = capture_hardware_profile()
        >>> estimate = estimate_training_duration(
        ...     num_samples=100000,
        ...     num_epochs=10,
        ...     model_params=1000000,
        ...     hardware_profile=profile
        ... )
        >>> print(f"Estimated time: {estimate['estimated_minutes']:.1f} minutes")
        >>> if estimate['is_long_running']:
        ...     print("This experiment requires user approval for long-running mode")
    """
    # GPU TFLOPs lookup table (FP32 performance)
    GPU_TFLOPS = {
        "V100": 7.0,
        "A100": 19.5,
        "H100": 60.0,
        "T4": 8.1,
        "P100": 4.7,
        "K80": 2.91,
        "RTX 3090": 35.6,
        "RTX 4090": 82.6,
        "A6000": 38.7,
    }

    # Determine GPU TFLOPs
    gpu_tflops = 5.0  # Conservative default for unknown GPUs
    confidence = "LOW"  # Start with low confidence

    if hardware_profile.get("gpu"):
        gpu_name = hardware_profile["gpu"]["name"]

        # Try exact match first
        if gpu_name in GPU_TFLOPS:
            gpu_tflops = GPU_TFLOPS[gpu_name]
            confidence = "HIGH"
        else:
            # Try partial match (e.g., "NVIDIA V100-SXM2-16GB" matches "V100")
            for known_gpu, tflops in GPU_TFLOPS.items():
                if known_gpu in gpu_name:
                    gpu_tflops = tflops
                    confidence = "MEDIUM"
                    break
            else:
                # Unknown GPU, use default
                logger.info(f"Unknown GPU model '{gpu_name}', using default {gpu_tflops} TFLOPs")
                confidence = "LOW"
    else:
        # No GPU detected - use CPU fallback (very slow)
        logger.warning("No GPU detected, training will be slow")
        gpu_tflops = 0.1  # CPU is ~50x slower than low-end GPU
        confidence = "LOW"

    # Compute total FLOPs required
    # 6 * params for forward pass (2x) + backward pass (4x)
    compute_per_sample = 6 * model_params
    total_compute = compute_per_sample * num_samples * num_epochs

    # Convert to time (with 50% efficiency factor)
    theoretical_seconds = total_compute / (gpu_tflops * 1e12)
    estimated_seconds = theoretical_seconds * 2  # 50% efficiency

    # Determine if long-running (> 10 minutes)
    is_long_running = estimated_seconds > 600

    return DurationEstimate(
        estimated_seconds=estimated_seconds,
        estimated_minutes=estimated_seconds / 60,
        estimated_hours=estimated_seconds / 3600,
        is_long_running=is_long_running,
        requires_user_confirmation=is_long_running,
        gpu_tflops=gpu_tflops,
        confidence=confidence,
    )


def estimate_eda_duration(
    num_rows: int,
    num_columns: int,
    hardware_profile: dict,
) -> DurationEstimate:
    """
    Estimate exploratory data analysis (EDA) duration based on data size.

    Uses simpler heuristic: ~10 rows/ms for profiling operations.
    Memory-constrained if data size exceeds available memory.

    Args:
        num_rows: Number of rows in dataset
        num_columns: Number of columns in dataset
        hardware_profile: Hardware profile from capture_hardware_profile()

    Returns:
        DurationEstimate with time estimates and is_long_running flag

    Examples:
        >>> profile = capture_hardware_profile()
        >>> estimate = estimate_eda_duration(
        ...     num_rows=1000000,
        ...     num_columns=50,
        ...     hardware_profile=profile
        ... )
        >>> print(f"EDA estimated time: {estimate['estimated_minutes']:.1f} minutes")
    """
    # Estimate data size in memory (rough approximation)
    # Assume 8 bytes per numeric value + overhead
    estimated_data_size_gb = (num_rows * num_columns * 8) / (1024**3)

    # Check if memory-constrained
    available_memory_gb = hardware_profile.get("memory", {}).get("available_gb", 8.0)
    is_memory_constrained = estimated_data_size_gb > (available_memory_gb * 0.5)

    # Base heuristic: ~10 rows/ms for profiling
    base_seconds = num_rows / 10000

    # Add column overhead (more columns = more profiling work)
    column_factor = 1 + (num_columns / 100)
    estimated_seconds = base_seconds * column_factor

    # If memory-constrained, operations will be slower (disk I/O)
    if is_memory_constrained:
        estimated_seconds *= 3  # 3x slower with disk operations
        confidence = "MEDIUM"
        logger.info(
            f"Data size ({estimated_data_size_gb:.1f} GB) exceeds available memory "
            f"({available_memory_gb:.1f} GB), EDA may be slower"
        )
    else:
        confidence = "HIGH"

    # Minimum 1 second
    estimated_seconds = max(1.0, estimated_seconds)

    # Determine if long-running (> 10 minutes)
    is_long_running = estimated_seconds > 600

    return DurationEstimate(
        estimated_seconds=estimated_seconds,
        estimated_minutes=estimated_seconds / 60,
        estimated_hours=estimated_seconds / 3600,
        is_long_running=is_long_running,
        requires_user_confirmation=is_long_running,
        gpu_tflops=0.0,  # EDA doesn't use GPU
        confidence=confidence,
    )
