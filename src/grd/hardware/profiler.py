"""Hardware profiling for ML experiments - captures CPU, memory, disk, and GPU specs."""

import logging
from datetime import datetime
from typing import TypedDict, Optional

logger = logging.getLogger(__name__)


class CPUInfo(TypedDict):
    """CPU information."""
    brand: str
    architecture: str
    cores_physical: int
    cores_logical: int
    frequency_mhz: Optional[float]


class MemoryInfo(TypedDict):
    """Memory information."""
    total_gb: float
    available_gb: float


class DiskInfo(TypedDict):
    """Disk information."""
    total_gb: float
    free_gb: float


class GPUInfo(TypedDict):
    """GPU information."""
    name: str
    total_memory_gb: float
    device_count: int
    compute_capability: Optional[str]
    cuda_version: Optional[str]
    driver_version: Optional[str]


class HardwareProfile(TypedDict):
    """Complete hardware profile for reproducibility."""
    cpu: CPUInfo
    memory: MemoryInfo
    disk: DiskInfo
    gpu: Optional[GPUInfo]
    timestamp: str


def capture_hardware_profile() -> HardwareProfile:
    """
    Capture complete hardware context for reproducibility.

    Uses psutil for CPU/memory/disk, py-cpuinfo for CPU details,
    torch.cuda (preferred) or GPUtil (fallback) for GPU detection.

    Returns:
        HardwareProfile dict with cpu, memory, disk, gpu (or None), timestamp

    Examples:
        >>> profile = capture_hardware_profile()
        >>> print(f"CPU: {profile['cpu']['brand']}")
        >>> if profile['gpu']:
        ...     print(f"GPU: {profile['gpu']['name']}")
    """
    profile: HardwareProfile = {
        "cpu": _capture_cpu_info(),
        "memory": _capture_memory_info(),
        "disk": _capture_disk_info(),
        "gpu": _capture_gpu_info(),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    return profile


def _capture_cpu_info() -> CPUInfo:
    """Capture CPU information using psutil and py-cpuinfo."""
    try:
        import psutil
        import cpuinfo

        cpu_info_dict = cpuinfo.get_cpu_info()
        cpu_freq = psutil.cpu_freq()

        return CPUInfo(
            brand=cpu_info_dict.get("brand_raw", "Unknown"),
            architecture=cpu_info_dict.get("arch", "Unknown"),
            cores_physical=psutil.cpu_count(logical=False) or 0,
            cores_logical=psutil.cpu_count(logical=True) or 0,
            frequency_mhz=cpu_freq.current if cpu_freq else None,
        )
    except ImportError as e:
        logger.warning(f"CPU profiling libraries not available: {e}")
        return CPUInfo(
            brand="Unknown",
            architecture="Unknown",
            cores_physical=0,
            cores_logical=0,
            frequency_mhz=None,
        )
    except Exception as e:
        logger.warning(f"Error capturing CPU info: {e}")
        return CPUInfo(
            brand="Unknown",
            architecture="Unknown",
            cores_physical=0,
            cores_logical=0,
            frequency_mhz=None,
        )


def _capture_memory_info() -> MemoryInfo:
    """Capture memory information using psutil."""
    try:
        import psutil

        mem = psutil.virtual_memory()
        return MemoryInfo(
            total_gb=mem.total / (1024**3),
            available_gb=mem.available / (1024**3),
        )
    except ImportError as e:
        logger.warning(f"psutil not available for memory profiling: {e}")
        return MemoryInfo(total_gb=0.0, available_gb=0.0)
    except Exception as e:
        logger.warning(f"Error capturing memory info: {e}")
        return MemoryInfo(total_gb=0.0, available_gb=0.0)


def _capture_disk_info() -> DiskInfo:
    """Capture disk information using psutil."""
    try:
        import psutil

        disk = psutil.disk_usage('/')
        return DiskInfo(
            total_gb=disk.total / (1024**3),
            free_gb=disk.free / (1024**3),
        )
    except ImportError as e:
        logger.warning(f"psutil not available for disk profiling: {e}")
        return DiskInfo(total_gb=0.0, free_gb=0.0)
    except Exception as e:
        logger.warning(f"Error capturing disk info: {e}")
        return DiskInfo(total_gb=0.0, free_gb=0.0)


def _capture_gpu_info() -> Optional[GPUInfo]:
    """
    Capture GPU information using torch.cuda (preferred) or GPUtil (fallback).

    Returns None if no GPU detected or libraries unavailable.
    """
    # Try PyTorch first (most reliable for ML workloads)
    try:
        import torch

        if torch.cuda.is_available():
            gpu_props = torch.cuda.get_device_properties(0)
            return GPUInfo(
                name=gpu_props.name,
                total_memory_gb=gpu_props.total_memory / (1024**3),
                device_count=torch.cuda.device_count(),
                compute_capability=f"{gpu_props.major}.{gpu_props.minor}",
                cuda_version=torch.version.cuda or "Unknown",
                driver_version=None,  # torch.cuda doesn't provide driver version
            )
    except ImportError:
        logger.debug("PyTorch not available, trying GPUtil fallback")
    except Exception as e:
        logger.warning(f"Error using torch.cuda for GPU detection: {e}")

    # Fallback to GPUtil
    try:
        import GPUtil

        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]  # Use first GPU
            return GPUInfo(
                name=gpu.name,
                total_memory_gb=gpu.memoryTotal / 1024,  # GPUtil returns MB
                device_count=len(gpus),
                compute_capability=None,  # GPUtil doesn't provide this
                cuda_version=None,  # GPUtil doesn't provide this
                driver_version=gpu.driver,
            )
    except ImportError:
        logger.debug("GPUtil not available for GPU detection")
    except Exception as e:
        logger.warning(f"Error using GPUtil for GPU detection: {e}")

    # No GPU detected or libraries unavailable
    logger.info("No GPU detected or GPU libraries unavailable")
    return None
