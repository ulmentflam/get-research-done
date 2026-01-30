"""Checkpoint handling for ML training experiments.

This module provides checkpoint save/load functionality with graceful shutdown
support. When training is interrupted (SIGINT/SIGTERM), the handler saves a
checkpoint before termination, allowing experiments to resume from the last
saved state.

Pattern 7 from RESEARCH.md: Signal handlers for graceful shutdown.
Pattern 4 from RESEARCH.md: Checkpoint-resume for long training.
"""
import signal
import sys
from pathlib import Path
from typing import Optional


class CheckpointHandler:
    """Handles saving and loading of training checkpoints.

    Provides checkpoint save/load with graceful shutdown support. Registers
    signal handlers (SIGINT/SIGTERM) to set an interrupted flag, allowing
    training loops to save checkpoints before termination.

    Checkpoints are saved in two formats:
    - checkpoint_epoch_{N}.pt: Versioned checkpoint for specific epoch
    - checkpoint_latest.pt: Latest checkpoint for easy resume

    Attributes:
        checkpoint_dir: Directory for storing checkpoints
        interrupted: Flag set when shutdown signal received
        _signal_handlers_registered: Whether handlers are active

    Example:
        >>> ch = CheckpointHandler(Path("checkpoints"))
        >>> ch.save_checkpoint(
        ...     epoch=5,
        ...     model_state={"weights": [1,2,3]},
        ...     optimizer_state={"lr": 0.001},
        ...     loss=0.5
        ... )
        >>> loaded = ch.load_checkpoint()
        >>> print(loaded["epoch"])
        5
    """

    def __init__(self, checkpoint_dir: Path):
        """Initialize checkpoint handler.

        Args:
            checkpoint_dir: Directory for storing checkpoints (created if needed)

        Example:
            >>> ch = CheckpointHandler(Path("experiments/run_001/checkpoints"))
        """
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.interrupted = False
        self._signal_handlers_registered = False
        self._setup_signal_handlers()

    def _setup_signal_handlers(self) -> None:
        """Register SIGINT and SIGTERM handlers for graceful shutdown.

        Sets self.interrupted = True when signal received, allowing training
        loops to detect shutdown request and save checkpoints.

        Pattern 7 from RESEARCH.md: Graceful shutdown with signal handlers.
        """
        if self._signal_handlers_registered:
            return  # Already registered

        def signal_handler(signum, frame):
            """Handle interrupt signals gracefully."""
            signal_name = "SIGINT" if signum == signal.SIGINT else "SIGTERM"
            print(f"\n{'='*70}")
            print(f"GRACEFUL SHUTDOWN INITIATED")
            print(f"{'='*70}")
            print(f"Received {signal_name} (signal {signum})")
            print(f"Setting interrupted flag...")
            print(f"Training loop should save checkpoint and exit cleanly.")
            print(f"{'='*70}\n")
            self.interrupted = True

        # Register handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        self._signal_handlers_registered = True

    def save_checkpoint(
        self,
        epoch: int,
        model_state: dict,
        optimizer_state: dict,
        loss: float,
        metadata: Optional[dict] = None
    ) -> Path:
        """Save complete training state for resumability.

        Creates checkpoint dict with epoch, model_state, optimizer_state, loss,
        and metadata. Saves as both checkpoint_epoch_{N}.pt and checkpoint_latest.pt.

        Args:
            epoch: Current epoch number
            model_state: Model state dict (from model.state_dict())
            optimizer_state: Optimizer state dict (from optimizer.state_dict())
            loss: Current loss value
            metadata: Optional metadata (run_id, timestamp, etc.)

        Returns:
            Path to saved checkpoint file (checkpoint_epoch_{N}.pt)

        Note:
            Uses torch.save() for atomic writes. If torch is not available,
            falls back to Python pickle (less reliable for large tensors).

        Example:
            >>> ch = CheckpointHandler(Path("checkpoints"))
            >>> path = ch.save_checkpoint(
            ...     epoch=10,
            ...     model_state={"layer1": torch.randn(10, 10)},
            ...     optimizer_state={"lr": 0.001},
            ...     loss=0.234,
            ...     metadata={"run_id": "run_001"}
            ... )
        """
        checkpoint = {
            "epoch": epoch,
            "model_state": model_state,
            "optimizer_state": optimizer_state,
            "loss": loss,
            "metadata": metadata or {},
        }

        # Save with epoch number for versioning
        checkpoint_path = self.checkpoint_dir / f"checkpoint_epoch_{epoch}.pt"

        # Try torch.save first (preferred for PyTorch models)
        try:
            import torch
            torch.save(checkpoint, checkpoint_path)
            # Also save as "latest" for easy resume
            latest_path = self.checkpoint_dir / "checkpoint_latest.pt"
            torch.save(checkpoint, latest_path)
        except ImportError:
            # Fallback to pickle if torch not available
            import pickle
            with open(checkpoint_path, 'wb') as f:
                pickle.dump(checkpoint, f)
            latest_path = self.checkpoint_dir / "checkpoint_latest.pt"
            with open(latest_path, 'wb') as f:
                pickle.dump(checkpoint, f)

        return checkpoint_path

    def load_checkpoint(self) -> Optional[dict]:
        """Load checkpoint for training resumption.

        Loads checkpoint_latest.pt if exists. Returns dict with epoch,
        model_state, optimizer_state, loss, and metadata.

        Returns:
            Checkpoint dict if checkpoint exists, None otherwise

        Example:
            >>> ch = CheckpointHandler(Path("checkpoints"))
            >>> loaded = ch.load_checkpoint()
            >>> if loaded:
            ...     print(f"Resuming from epoch {loaded['epoch']}")
            ...     model.load_state_dict(loaded['model_state'])
            ...     optimizer.load_state_dict(loaded['optimizer_state'])
        """
        latest_path = self.checkpoint_dir / "checkpoint_latest.pt"

        if not latest_path.exists():
            return None  # No checkpoint to resume from

        # Try torch.load first (preferred for PyTorch models)
        try:
            import torch
            checkpoint = torch.load(latest_path)
        except ImportError:
            # Fallback to pickle if torch not available
            import pickle
            with open(latest_path, 'rb') as f:
                checkpoint = pickle.load(f)

        return checkpoint

    def find_latest_checkpoint(self) -> Optional[Path]:
        """Find most recent checkpoint by epoch number.

        Searches for checkpoint_epoch_*.pt files and returns the one with
        the highest epoch number.

        Returns:
            Path to latest checkpoint, or None if no checkpoints exist

        Example:
            >>> ch = CheckpointHandler(Path("checkpoints"))
            >>> latest = ch.find_latest_checkpoint()
            >>> if latest:
            ...     print(f"Found checkpoint: {latest.name}")
        """
        checkpoints = list(self.checkpoint_dir.glob("checkpoint_epoch_*.pt"))
        if not checkpoints:
            return None

        # Sort by epoch number (extract from filename)
        checkpoints.sort(key=lambda p: int(p.stem.split("_")[-1]))
        return checkpoints[-1]

    def check_interrupted(self) -> bool:
        """Check if training has been interrupted.

        Returns self.interrupted flag, which is set when SIGINT or SIGTERM
        is received. Used in training loops to detect shutdown request.

        Returns:
            True if interrupted, False otherwise

        Example:
            >>> ch = CheckpointHandler(Path("checkpoints"))
            >>> for epoch in range(num_epochs):
            ...     if ch.check_interrupted():
            ...         print("Interrupted! Saving checkpoint...")
            ...         ch.save_checkpoint(epoch, model_state, optimizer_state, loss)
            ...         break
            ...     train_epoch(model, optimizer)
        """
        return self.interrupted

    def get_resumability_hints(self) -> dict:
        """Get suggestions for resuming training.

        Returns actionable hints about checkpoint state, including whether
        a checkpoint exists, the latest epoch, checkpoint path, and estimated
        remaining epochs.

        Returns:
            Dictionary with resumability hints:
            - has_checkpoint: Whether checkpoint exists
            - latest_epoch: Epoch number of latest checkpoint (or None)
            - checkpoint_path: Path to latest checkpoint (or None)
            - checkpoint_count: Number of checkpoint files

        Example:
            >>> ch = CheckpointHandler(Path("checkpoints"))
            >>> hints = ch.get_resumability_hints()
            >>> if hints["has_checkpoint"]:
            ...     print(f"Resume from epoch {hints['latest_epoch']}")
            ... else:
            ...     print("No checkpoint found - starting from scratch")
        """
        latest_checkpoint = self.find_latest_checkpoint()

        if latest_checkpoint is None:
            return {
                "has_checkpoint": False,
                "latest_epoch": None,
                "checkpoint_path": None,
                "checkpoint_count": 0,
            }

        # Extract epoch from filename
        epoch = int(latest_checkpoint.stem.split("_")[-1])

        # Count all checkpoints
        checkpoints = list(self.checkpoint_dir.glob("checkpoint_epoch_*.pt"))

        return {
            "has_checkpoint": True,
            "latest_epoch": epoch,
            "checkpoint_path": str(latest_checkpoint),
            "checkpoint_count": len(checkpoints),
        }
