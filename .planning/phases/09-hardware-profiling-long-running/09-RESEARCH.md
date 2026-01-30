# Phase 9: Hardware Profiling & Long-Running Experiments - Research

**Researched:** 2026-01-30
**Domain:** Hardware detection, experiment timeout management, checkpoint resumability
**Confidence:** HIGH

## Summary

This phase enables reproducible ML experiments by capturing hardware context and handling training runs that exceed standard timeouts. The research identifies proven libraries for hardware profiling (psutil, GPUtil, py-cpuinfo), established patterns for timeout bypass (asyncio context managers, subprocess management), and standard checkpoint strategies (PyTorch state_dict, MLflow system metrics).

**Key findings:**
- Hardware profiling requires combining multiple libraries: psutil for CPU/memory/disk, GPUtil for NVIDIA GPU metrics, py-cpuinfo for detailed CPU specs
- PyTorch and TensorFlow provide native GPU detection that should be preferred over third-party tools when available
- Python 3.11+ asyncio.timeout() is the modern approach for timeout management, replacing older wait_for() patterns
- MLflow provides standardized system metrics tracking including GPU utilization, memory, and power consumption
- Checkpoints must include model state, optimizer state, epoch number, and loss value for proper resumability
- Long-running experiments require graceful shutdown handlers (SIGTERM/SIGINT) to save checkpoints before termination

**Primary recommendation:** Use psutil + GPUtil + torch.cuda (or tf.config) for hardware profiling, asyncio.timeout() for timeout management, and MLflow system metrics for standardized logging. Capture hardware context during EDA phase and store in DATA_REPORT.md. Implement checkpoint-resume pattern with session-level user approval for long-running experiments.

## Standard Stack

The established libraries/tools for this domain:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| psutil | 7.2.2+ | CPU, memory, disk, network monitoring | Cross-platform, actively maintained (Jan 2026), standard for system monitoring |
| GPUtil | 1.4.0+ | NVIDIA GPU status via nvidia-smi | Lightweight, simple API, widely used for GPU selection in ML |
| py-cpuinfo | 9.0.0+ | Detailed CPU information | Pure Python, cross-platform (Linux/macOS/Windows), no compilation needed |
| tqdm | 5.0+ | Progress bars for experiments | Standard for ML training loops, minimal overhead (60ns/iter) |
| rich | 14.1.0+ | Advanced progress tracking with multiple tasks | Modern alternative to tqdm, excellent for concurrent task tracking |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| nvidia-ml-py | 12.0+ | NVIDIA Management Library bindings | When GPU metrics beyond nvidia-smi are needed (MLflow requirement) |
| pyrsmi | Latest | AMD GPU monitoring | When targeting AMD/HIP GPUs instead of NVIDIA |
| graceful-shutdown | 1.0+ | Signal handling for cleanup | For Docker/containerized long-running experiments |

### Framework-Native (Preferred)
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| torch.cuda | PyTorch 2.10+ | PyTorch GPU detection | Always use for PyTorch projects - more reliable than GPUtil |
| tf.config.experimental | TensorFlow 2.16+ | TensorFlow GPU detection | Always use for TensorFlow projects |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| tqdm | rich | Rich provides better multi-task tracking but higher complexity |
| GPUtil | pynvml | pynvml offers more metrics but more complex API |
| asyncio.timeout() | subprocess.run(timeout=X) | subprocess timeout for shell commands, asyncio for Python tasks |

**Installation:**
```bash
# Core hardware profiling
pip install psutil gputil py-cpuinfo

# Progress tracking
pip install tqdm rich

# MLflow system metrics (requires NVIDIA GPU drivers)
pip install nvidia-ml-py  # or pyrsmi for AMD

# Graceful shutdown
pip install graceful-shutdown
```

## Architecture Patterns

### Recommended Project Structure
```
src/agents/
├── explorer/
│   ├── hardware_profiler.py    # Captures hardware context during EDA
│   └── data_report.py           # Writes hardware section to DATA_REPORT.md
├── researcher/
│   ├── experiment_manager.py   # Handles timeout bypass with user confirmation
│   ├── checkpoint_handler.py   # Saves/loads experiment checkpoints
│   └── duration_estimator.py   # Estimates completion time from hardware + data
└── shared/
    ├── hardware_context.py      # Hardware profile data structure
    └── timeout_manager.py       # Timeout bypass context manager
```

### Pattern 1: Hardware Profiling on EDA Start
**What:** Capture complete hardware profile at the beginning of exploratory data analysis
**When to use:** Every time Explorer agent starts EDA phase
**Example:**
```python
# Source: psutil docs + GPUtil + py-cpuinfo
import psutil
import GPUtil
import cpuinfo
import torch  # or tensorflow as tf

def capture_hardware_profile():
    """Capture complete hardware context for reproducibility."""
    profile = {
        # CPU information
        "cpu": {
            "brand": cpuinfo.get_cpu_info()["brand_raw"],
            "architecture": cpuinfo.get_cpu_info()["arch"],
            "cores_physical": psutil.cpu_count(logical=False),
            "cores_logical": psutil.cpu_count(logical=True),
            "frequency_mhz": psutil.cpu_freq().current if psutil.cpu_freq() else None,
        },
        # Memory information
        "memory": {
            "total_gb": psutil.virtual_memory().total / (1024**3),
            "available_gb": psutil.virtual_memory().available / (1024**3),
        },
        # Disk information
        "disk": {
            "total_gb": psutil.disk_usage('/').total / (1024**3),
            "free_gb": psutil.disk_usage('/').free / (1024**3),
        },
        # GPU information (if available)
        "gpu": None
    }

    # Try PyTorch first (most reliable)
    if torch.cuda.is_available():
        gpu_props = torch.cuda.get_device_properties(0)
        profile["gpu"] = {
            "name": gpu_props.name,
            "compute_capability": f"{gpu_props.major}.{gpu_props.minor}",
            "total_memory_gb": gpu_props.total_memory / (1024**3),
            "cuda_version": torch.version.cuda,
            "device_count": torch.cuda.device_count(),
        }
    # Fallback to GPUtil
    elif GPUtil.getAvailable():
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]
            profile["gpu"] = {
                "name": gpu.name,
                "total_memory_gb": gpu.memoryTotal / 1024,
                "driver_version": gpu.driver,
                "device_count": len(gpus),
            }

    return profile
```

### Pattern 2: Duration Estimation from Hardware Context
**What:** Estimate experiment runtime based on hardware specs and data size
**When to use:** Before starting Researcher experiments, especially training
**Example:**
```python
# Source: Epoch AI, Medium training time estimation
def estimate_training_duration(
    num_samples: int,
    num_epochs: int,
    model_params: int,
    hardware_profile: dict,
    batch_size: int = 32
) -> dict:
    """Estimate training time based on hardware and data."""

    # Get GPU throughput (TFLOPs)
    gpu_tflops = {
        "V100": 7.0,
        "A100": 19.5,
        "H100": 60.0,
        "T4": 8.1,
    }.get(hardware_profile["gpu"]["name"].split()[0], 5.0)  # default conservative

    # Estimate compute per sample (6 * params for forward+backward)
    compute_per_sample = 6 * model_params
    total_compute = compute_per_sample * num_samples * num_epochs

    # Convert to time (with 50% efficiency factor)
    theoretical_seconds = total_compute / (gpu_tflops * 1e12)
    estimated_seconds = theoretical_seconds * 2  # 50% efficiency

    # Determine if long-running (> 10 minutes)
    is_long_running = estimated_seconds > 600

    return {
        "estimated_seconds": estimated_seconds,
        "estimated_minutes": estimated_seconds / 60,
        "estimated_hours": estimated_seconds / 3600,
        "is_long_running": is_long_running,
        "requires_user_confirmation": is_long_running,
        "gpu_tflops": gpu_tflops,
        "total_tflops": total_compute / 1e12,
    }
```

### Pattern 3: Timeout Bypass with User Confirmation
**What:** Session-level approval for long-running experiments, no repeated prompts
**When to use:** When estimated duration > 10 minutes
**Example:**
```python
# Source: Python asyncio docs 3.11+
import asyncio
from contextlib import asynccontextmanager

class ExperimentTimeoutManager:
    """Manages timeouts for experiments with session-level approval."""

    def __init__(self):
        self.long_running_approved = False
        self.session_timeout = None

    async def request_long_running_approval(self, estimated_minutes: float):
        """Request user approval for long-running experiment (once per session)."""
        if self.long_running_approved:
            return True  # Already approved this session

        print(f"\nThis experiment will take approximately {estimated_minutes:.1f} minutes.")
        print("This exceeds the standard 10-minute task timeout.")
        response = input("Approve long-running mode for this session? (yes/no): ")

        if response.lower() in ["yes", "y"]:
            self.long_running_approved = True
            self.session_timeout = None  # No timeout
            print("Long-running mode approved. No further prompts this session.")
            return True
        else:
            self.session_timeout = 600  # 10 minute default
            return False

    @asynccontextmanager
    async def experiment_context(self, estimated_seconds: float):
        """Context manager for experiment execution with appropriate timeout."""
        if estimated_seconds > 600 and not self.long_running_approved:
            approved = await self.request_long_running_approval(estimated_seconds / 60)
            if not approved:
                raise TimeoutError("User declined long-running experiment approval")

        # Use asyncio.timeout() for Python 3.11+
        timeout_delay = self.session_timeout if self.session_timeout else None

        try:
            async with asyncio.timeout(timeout_delay) as cm:
                yield cm
        except TimeoutError:
            print(f"Experiment timed out after {timeout_delay} seconds")
            raise
```

### Pattern 4: Checkpoint-Resume for Long Training
**What:** Save complete training state at regular intervals for resumability
**When to use:** All training experiments, especially long-running ones
**Example:**
```python
# Source: PyTorch official docs
import torch
from pathlib import Path

class CheckpointHandler:
    """Handles saving and loading of training checkpoints."""

    def __init__(self, checkpoint_dir: Path):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def save_checkpoint(
        self,
        epoch: int,
        model: torch.nn.Module,
        optimizer: torch.optim.Optimizer,
        loss: float,
        metadata: dict = None
    ):
        """Save complete training state for resumability."""
        checkpoint = {
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "loss": loss,
            "metadata": metadata or {},
        }

        # Save with epoch number
        checkpoint_path = self.checkpoint_dir / f"checkpoint_epoch_{epoch}.pt"
        torch.save(checkpoint, checkpoint_path)

        # Also save as "latest" for easy resume
        latest_path = self.checkpoint_dir / "checkpoint_latest.pt"
        torch.save(checkpoint, latest_path)

        return checkpoint_path

    def load_checkpoint(self, model: torch.nn.Module, optimizer: torch.optim.Optimizer):
        """Load checkpoint for training resumption."""
        latest_path = self.checkpoint_dir / "checkpoint_latest.pt"

        if not latest_path.exists():
            return None  # No checkpoint to resume from

        checkpoint = torch.load(latest_path)
        model.load_state_dict(checkpoint["model_state_dict"])
        optimizer.load_state_dict(checkpoint["optimizer_state_dict"])

        return {
            "epoch": checkpoint["epoch"],
            "loss": checkpoint["loss"],
            "metadata": checkpoint.get("metadata", {}),
        }

    def find_latest_checkpoint(self) -> Path | None:
        """Find most recent checkpoint by epoch number."""
        checkpoints = list(self.checkpoint_dir.glob("checkpoint_epoch_*.pt"))
        if not checkpoints:
            return None

        # Sort by epoch number
        checkpoints.sort(key=lambda p: int(p.stem.split("_")[-1]))
        return checkpoints[-1]
```

### Pattern 5: Progress Tracking with Rich
**What:** Display real-time progress with estimated completion time
**When to use:** Long-running experiments to provide user visibility
**Example:**
```python
# Source: Rich documentation
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn, TimeRemainingColumn
import time

def train_with_progress(num_epochs: int, steps_per_epoch: int):
    """Training loop with rich progress tracking."""

    with Progress(
        SpinnerColumn(),
        *Progress.get_default_columns(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
    ) as progress:

        # Overall training progress
        train_task = progress.add_task("[cyan]Training...", total=num_epochs)

        for epoch in range(num_epochs):
            # Epoch progress
            epoch_task = progress.add_task(
                f"[green]Epoch {epoch+1}/{num_epochs}",
                total=steps_per_epoch
            )

            for step in range(steps_per_epoch):
                # Simulate training step
                time.sleep(0.01)

                # Update progress
                progress.update(epoch_task, advance=1)

            # Epoch complete
            progress.update(train_task, advance=1)
            progress.remove_task(epoch_task)
```

### Pattern 6: MLflow System Metrics Integration
**What:** Log hardware metrics automatically during experiments
**When to use:** All Researcher experiments for reproducibility tracking
**Example:**
```python
# Source: MLflow system metrics documentation
import mlflow

def run_experiment_with_metrics():
    """Run experiment with automatic system metrics logging."""

    # Enable system metrics (requires nvidia-ml-py for GPU)
    mlflow.enable_system_metrics_logging()

    with mlflow.start_run(log_system_metrics=True):
        # Log hardware profile as parameters
        hardware = capture_hardware_profile()
        mlflow.log_params({
            "cpu_cores": hardware["cpu"]["cores_physical"],
            "memory_gb": hardware["memory"]["total_gb"],
            "gpu_name": hardware["gpu"]["name"] if hardware["gpu"] else "none",
            "cuda_version": hardware["gpu"]["cuda_version"] if hardware["gpu"] else "none",
        })

        # Train model (system metrics logged automatically every 10s)
        # Metrics: system/cpu_utilization_percentage
        #          system/gpu_utilization_percentage
        #          system/gpu_memory_usage_megabytes
        #          system/gpu_power_usage_watts
        train_model()
```

### Pattern 7: Graceful Shutdown with Signal Handlers
**What:** Save checkpoint and cleanup when interrupted (Ctrl+C, SIGTERM)
**When to use:** Long-running experiments that might be interrupted
**Example:**
```python
# Source: Python signal handling best practices
import signal
import sys

class GracefulExperiment:
    """Experiment that saves checkpoint on interruption."""

    def __init__(self, checkpoint_handler: CheckpointHandler):
        self.checkpoint_handler = checkpoint_handler
        self.interrupted = False
        self.current_epoch = 0

        # Register signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle interrupt signals gracefully."""
        print(f"\nReceived signal {signum}. Saving checkpoint...")
        self.interrupted = True

    def train(self, model, optimizer, num_epochs):
        """Training loop with graceful shutdown."""
        for epoch in range(num_epochs):
            if self.interrupted:
                print(f"Saving emergency checkpoint at epoch {epoch}...")
                self.checkpoint_handler.save_checkpoint(
                    epoch=epoch,
                    model=model,
                    optimizer=optimizer,
                    loss=self.last_loss,
                    metadata={"interrupted": True}
                )
                sys.exit(0)

            self.current_epoch = epoch
            self.last_loss = train_epoch(model, optimizer)

            # Regular checkpoint
            if epoch % 5 == 0:
                self.checkpoint_handler.save_checkpoint(
                    epoch, model, optimizer, self.last_loss
                )
```

### Anti-Patterns to Avoid

- **Hard-coding GPU indices:** Use torch.cuda.current_device() or GPUtil.getAvailable() instead of assuming GPU 0
- **Ignoring GPU unavailability:** Always check torch.cuda.is_available() before GPU operations
- **Saving only model weights:** Must include optimizer state, epoch, and loss for proper resumability
- **Blocking on subprocess.run() without timeout:** Use timeout parameter or asyncio for non-blocking execution
- **Using nvidia-smi output parsing:** Use GPUtil or torch.cuda instead of parsing nvidia-smi text output
- **Synchronous checkpointing without async:** Large checkpoints block training; use async checkpointing for models >1GB

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| GPU detection | Parsing nvidia-smi output | GPUtil or torch.cuda.get_device_properties() | nvidia-smi output format varies by driver version, GPUtil handles edge cases |
| CPU info | Reading /proc/cpuinfo | py-cpuinfo | Cross-platform (works on Windows/macOS), handles various CPU architectures |
| Progress bars | Print with percentage | tqdm or rich | Smart time estimation, handles nested loops, minimal overhead |
| Timeout management | Threading with timers | asyncio.timeout() (Python 3.11+) | Built-in, handles cancellation properly, no race conditions |
| System monitoring | Custom psutil wrapper | MLflow system metrics | Standard format, automatic logging, integrates with experiment tracking |
| Checkpoint corruption | Manual file locking | torch.save with atomic writes | Handles incomplete saves, built-in validation |

**Key insight:** Hardware profiling requires combining multiple specialized libraries because no single library covers CPU, GPU, memory, and disk comprehensively. Using framework-native tools (torch.cuda, tf.config) is always more reliable than third-party wrappers.

## Common Pitfalls

### Pitfall 1: Using nvidia-smi GPU Utilization as Performance Metric
**What goes wrong:** GPU utilization from nvidia-smi shows only the fraction of time a kernel is running, not how efficiently the GPU is used or how many CUDA cores are active.
**Why it happens:** nvidia-smi is the most visible tool, and "100% GPU utilization" seems like good performance.
**How to avoid:** Use MLflow system metrics or profiling tools (NVIDIA Nsight) to understand true GPU efficiency. Monitor memory bandwidth and compute throughput, not just utilization percentage.
**Warning signs:** High GPU utilization but slow training, or GPU utilization fluctuating wildly.

### Pitfall 2: Checkpoint Corruption During Training Interruption
**What goes wrong:** Checkpoint file is corrupted or incomplete because training was killed while writing checkpoint. On resume, model loads garbage or crashes.
**Why it happens:** Without atomic writes, checkpoint file can be partially written if process is killed. Training process modifies checkpoint during write.
**How to avoid:** Use torch.save() which performs atomic writes. Save to temporary file then rename. Validate checkpoint after saving. Keep previous checkpoint until new one is validated.
**Warning signs:** "EOFError: Ran out of input" when loading checkpoint, inconsistent loss values after resume, checkpoint file size varies unexpectedly.

### Pitfall 3: Race Conditions in Timeout Cleanup
**What goes wrong:** Process times out but cleanup code doesn't run, or runs partially, leaving GPU memory allocated or files locked.
**Why it happens:** Using subprocess with timeout kills process immediately without cleanup. Signal handlers race with timeout.
**How to avoid:** Use asyncio.timeout() with try/finally blocks for cleanup. For subprocesses, use process groups (os.killpg) to kill all children. Avoid daemon processes which don't allow cleanup.
**Warning signs:** GPU memory not freed after timeout, temp files accumulating, "device busy" errors.

### Pitfall 4: Running CPU Code on GPU Node
**What goes wrong:** Reserving expensive GPU resources but not using them because code doesn't have GPU support.
**Why it happens:** Assuming libraries automatically use GPU, or not checking torch.cuda.is_available() before GPU operations.
**How to avoid:** Always check hardware compatibility at start. Verify GPU is being used (torch.cuda.current_device(), check GPU memory usage). Test with small batch before full training.
**Warning signs:** Training is very slow despite GPU availability, GPU memory usage stays at baseline, nvidia-smi shows 0% utilization.

### Pitfall 5: Estimating Duration Without Hardware Context
**What goes wrong:** Tell user "this will take 5 minutes" based on local machine, but user's machine is much slower (or faster), leading to frustration.
**Why it happens:** Hard-coding duration estimates or using developer's hardware specs as baseline.
**How to avoid:** Always capture hardware profile first. Estimate based on GPU TFLOPs, CPU cores, and available memory. Run small benchmark before full experiment. Provide wide confidence interval.
**Warning signs:** User reports "experiment never finishes" or "estimated time way off," timeout issues on different hardware.

### Pitfall 6: Forgetting Optimizer State in Checkpoints
**What goes wrong:** Resume training but loss increases or training is unstable. Model weights are correct but optimizer momentum/learning rate schedule is reset.
**Why it happens:** Only saving model.state_dict() without optimizer.state_dict(), thinking weights are sufficient.
**How to avoid:** Always save optimizer state, epoch number, and loss value. Load all three when resuming. Test resume by comparing loss value immediately after loading.
**Warning signs:** Loss spikes after resume, learning rate restarts from initial value, momentum buffers reset.

### Pitfall 7: Session Timeout vs Task Timeout Confusion
**What goes wrong:** User approves "long-running mode" thinking it applies to one task, but it bypasses timeout for entire session, potentially allowing infinite loops.
**Why it happens:** Not clearly scoping approval to session vs individual task.
**How to avoid:** Clearly document session-level approval. Provide option to revert approval. Add maximum session timeout (e.g., 4 hours) even in long-running mode. Log approval in experiment metadata.
**Warning signs:** Experiments running much longer than estimated, user confused about why timeout was bypassed.

## Code Examples

Verified patterns from official sources:

### Hardware Profile Capture and Storage
```python
# Source: psutil + GPUtil + torch.cuda docs
import json
from pathlib import Path

def save_hardware_profile_to_report(profile: dict, report_path: Path):
    """Append hardware section to DATA_REPORT.md"""

    hardware_section = f"""
## Hardware Profile

**Captured:** {profile.get('timestamp', 'unknown')}

### CPU
- **Model:** {profile['cpu']['brand']}
- **Architecture:** {profile['cpu']['architecture']}
- **Cores:** {profile['cpu']['cores_physical']} physical, {profile['cpu']['cores_logical']} logical
- **Frequency:** {profile['cpu']['frequency_mhz']:.0f} MHz

### Memory
- **Total:** {profile['memory']['total_gb']:.1f} GB
- **Available:** {profile['memory']['available_gb']:.1f} GB

### Disk
- **Total:** {profile['disk']['total_gb']:.1f} GB
- **Free:** {profile['disk']['free_gb']:.1f} GB

### GPU
"""

    if profile['gpu']:
        hardware_section += f"""- **Model:** {profile['gpu']['name']}
- **Memory:** {profile['gpu']['total_memory_gb']:.1f} GB
- **CUDA Version:** {profile['gpu'].get('cuda_version', 'N/A')}
- **Compute Capability:** {profile['gpu'].get('compute_capability', 'N/A')}
- **Device Count:** {profile['gpu']['device_count']}
"""
    else:
        hardware_section += "- **Status:** No GPU detected\n"

    # Append to report
    with open(report_path, 'a') as f:
        f.write(hardware_section)
```

### Subprocess Timeout with Proper Cleanup
```python
# Source: Python subprocess documentation
import subprocess
import signal
import os

def run_with_timeout(command: list, timeout_seconds: int = 600):
    """Run subprocess with timeout and proper cleanup."""

    # Use process group for killing all children
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True  # Create new process group
    )

    try:
        stdout, stderr = process.communicate(timeout=timeout_seconds)
        return {
            "returncode": process.returncode,
            "stdout": stdout.decode(),
            "stderr": stderr.decode(),
        }
    except subprocess.TimeoutExpired:
        # Kill entire process group
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)

        # Wait for cleanup
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # Force kill if didn't terminate
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)

        raise TimeoutError(f"Command timed out after {timeout_seconds} seconds")
```

### PyTorch-Specific GPU Detection
```python
# Source: PyTorch official documentation
import torch

def get_pytorch_hardware_info():
    """Get comprehensive PyTorch hardware information."""

    info = {
        "pytorch_version": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "cuda_version": torch.version.cuda,
        "cudnn_version": torch.backends.cudnn.version(),
        "device_count": 0,
        "devices": [],
    }

    if torch.cuda.is_available():
        info["device_count"] = torch.cuda.device_count()

        for i in range(info["device_count"]):
            props = torch.cuda.get_device_properties(i)
            info["devices"].append({
                "id": i,
                "name": props.name,
                "compute_capability": f"{props.major}.{props.minor}",
                "total_memory_gb": props.total_memory / (1024**3),
                "multi_processor_count": props.multi_processor_count,
            })

    return info
```

### TensorFlow-Specific GPU Detection
```python
# Source: TensorFlow official documentation
import tensorflow as tf

def get_tensorflow_hardware_info():
    """Get comprehensive TensorFlow hardware information."""

    info = {
        "tensorflow_version": tf.__version__,
        "gpu_available": len(tf.config.list_physical_devices('GPU')) > 0,
        "devices": [],
    }

    gpus = tf.config.list_physical_devices('GPU')

    for gpu in gpus:
        details = tf.config.experimental.get_device_details(gpu)

        # Get memory info
        memory_info = tf.config.experimental.get_memory_info(gpu.name)

        info["devices"].append({
            "name": gpu.name,
            "device_name": details.get("device_name", "unknown"),
            "compute_capability": details.get("compute_capability", None),
            "current_memory_mb": memory_info["current"] / (1024**2),
            "peak_memory_mb": memory_info["peak"] / (1024**2),
        })

    return info
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| asyncio.wait_for() | asyncio.timeout() context manager | Python 3.11 (Oct 2022) | Cleaner syntax, better error handling, supports rescheduling |
| Manual nvidia-smi parsing | torch.cuda.get_device_properties() | PyTorch 1.0+ | More reliable, returns structured data, version-independent |
| tf.Session() for GPU info | tf.config.experimental.get_device_details() | TensorFlow 2.0 (Sep 2019) | Eager execution compatible, cleaner API |
| Synchronous checkpointing | Asynchronous checkpointing | PyTorch 2.0+ (Mar 2023) | 10x faster checkpoint saves for large models |
| subprocess.call() | subprocess.run() with timeout | Python 3.5 (Sep 2015) | Built-in timeout support, better error handling |
| Custom progress bars | tqdm with automatic estimation | tqdm 4.0+ (2016) | Smart time remaining, minimal overhead (60ns/iter) |

**Deprecated/outdated:**
- **wait_for() for timeouts:** Use asyncio.timeout() (Python 3.11+) for new code
- **nvidia-smi output parsing:** Use GPUtil or torch.cuda instead
- **Saving entire model with pickle:** Use state_dict() approach (PyTorch/TensorFlow recommended practice)
- **Manual system metrics collection:** Use MLflow system metrics logging (auto-logged every 10s)

## Open Questions

Things that couldn't be fully resolved:

1. **Optimal checkpoint frequency for different model sizes**
   - What we know: Should balance I/O overhead vs lost work on failure
   - What's unclear: Formula for optimal frequency based on model size and hardware
   - Recommendation: Default to every 5 epochs for small models (<100M params), every epoch for large models (>1B params). User can override.

2. **Claude Code agent timeout bypass mechanism**
   - What we know: Ralph Wiggum plugin enables autonomous long-running tasks, Ctrl+B moves sub-agents to background
   - What's unclear: How to programmatically bypass 10-minute timeout from within agent code
   - Recommendation: Use session-level user approval pattern, document that timeout is external constraint. Consider using Task tool with run_in_background parameter.

3. **Cross-platform CPU detection edge cases**
   - What we know: py-cpuinfo works on Linux/macOS/Windows but warns "raw fields may contain garbage"
   - What's unclear: Which fields are safe to rely on across platforms
   - Recommendation: Use brand, architecture, cores_physical, cores_logical (safe). Avoid raw vendor_id and brand_raw. Test on target platforms.

4. **AMD GPU support completeness**
   - What we know: pyrsmi exists for AMD GPUs, MLflow supports it
   - What's unclear: Feature parity with NVIDIA nvidia-ml-py, reliability of metrics
   - Recommendation: Document NVIDIA as primary target, AMD as experimental. Request AMD GPU access for testing if phase is critical.

## Sources

### Primary (HIGH confidence)
- [psutil 7.2.2 documentation](https://psutil.readthedocs.io/) - CPU, memory, disk, network monitoring
- [Python asyncio.timeout() documentation](https://docs.python.org/3/library/asyncio-task.html) - Timeout management (Python 3.11+)
- [PyTorch torch.cuda documentation](https://docs.pytorch.org/docs/stable/cuda.html) - GPU detection and properties
- [PyTorch saving and loading models](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html) - Checkpoint best practices
- [TensorFlow GPU configuration](https://www.tensorflow.org/api_docs/python/tf/config/experimental/get_device_details) - GPU device details
- [MLflow System Metrics](https://mlflow.org/docs/latest/ml/tracking/system-metrics/) - Automatic hardware metrics logging
- [Rich Progress documentation](https://rich.readthedocs.io/en/latest/progress.html) - Advanced progress tracking
- [tqdm documentation](https://tqdm.github.io/) - Progress bars

### Secondary (MEDIUM confidence)
- [GPUtil GitHub repository](https://github.com/anderskm/gputil) - NVIDIA GPU status via nvidia-smi
- [py-cpuinfo GitHub repository](https://github.com/workhorsy/py-cpuinfo) - Pure Python CPU information
- [Python subprocess documentation](https://docs.python.org/3/library/subprocess.html) - Timeout and cleanup
- [graceful-shutdown PyPI](https://pypi.org/project/graceful-shutdown/) - Signal handling library
- [Better Stack: Python Timeouts](https://betterstack.com/community/guides/scaling-python/python-timeouts/) - Comprehensive timeout guide
- [Run.ai: Checkpoint Best Practices](https://docs.run.ai/latest/Researcher/best-practices/save-dl-checkpoints/) - ML checkpoint strategies

### Tertiary (LOW confidence - require validation)
- [Ralph Wiggum plugin for Claude Code](https://looking4offswitch.github.io/blog/2026/01/04/ralph-wiggum-claude-code/) - Long-running task autonomy
- [Claude Code timeout prevention](https://claude-plugins.dev/skills/@jackspace/ClaudeSkillz/timeout-prevention) - Agent skill for timeout handling
- [Medium: Estimating Training Time](https://medium.com/@maxshapp/understanding-and-estimating-gpu-memory-demands-for-training-llms-in-practise-c5ef20a4baff) - GPU memory and duration estimation
- [DigitalOcean: Batch Size Optimization](https://www.digitalocean.com/community/tutorials/find-optimal-batch-size) - Finding optimal batch size for GPU
- [Princeton GPU Computing Guide](https://researchcomputing.princeton.edu/support/knowledge-base/gpu-computing) - Common GPU mistakes

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - All libraries actively maintained, official documentation verified, recent releases (psutil 7.2.2 Jan 2026)
- Architecture: HIGH - Patterns verified with official PyTorch/TensorFlow/Python docs, asyncio.timeout() is Python 3.11+ standard
- Pitfalls: MEDIUM-HIGH - Common mistakes documented in academic/industry sources, some from practical experience reports
- Claude Code integration: LOW - Ralph Wiggum plugin and timeout bypass are community-driven, not officially documented

**Research date:** 2026-01-30
**Valid until:** 2026-04-30 (90 days - hardware libraries are stable, but ML frameworks update frequently)

**Notes:**
- Python 3.11+ required for asyncio.timeout() (check runtime version)
- NVIDIA GPU support is more mature than AMD GPU support
- PyTorch 2.10+ and TensorFlow 2.16+ are current stable versions
- MLflow system metrics require nvidia-ml-py (NVIDIA) or pyrsmi (AMD) for GPU tracking
- Checkpoint async support requires PyTorch 2.0+ for 10x speedup on large models
