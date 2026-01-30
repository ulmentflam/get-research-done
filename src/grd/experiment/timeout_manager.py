"""Timeout management for long-running ML experiments.

This module provides session-level approval for experiments that exceed the
standard 10-minute timeout. Once approved, experiments can run without timeout
constraints for the duration of the session.

The manager does NOT use asyncio - it provides configuration for external timeout
handling. The actual timeout is applied by subprocess.run(timeout=X) or similar
in the caller.
"""
from datetime import datetime
from typing import Optional


class ExperimentTimeoutManager:
    """Manages timeouts for experiments with session-level approval.

    Provides session-level approval tracking for long-running experiments.
    Once a user approves long-running mode, all subsequent experiments in the
    session can bypass the standard timeout without repeated prompts.

    Attributes:
        default_timeout: Standard timeout in seconds (default: 600 = 10 minutes)
        long_running_approved: Whether long-running mode has been approved
        session_timeout: Active timeout value (None = no timeout)
        approval_metadata: Audit trail of approval events

    Example:
        >>> tm = ExperimentTimeoutManager()
        >>> tm.request_long_running_approval(30)  # 30 minutes
        >>> timeout = tm.get_timeout(3600)  # Returns None (no timeout)
    """

    def __init__(self, default_timeout: int = 600):
        """Initialize timeout manager.

        Args:
            default_timeout: Default timeout in seconds (default: 600 = 10 minutes)
        """
        self.default_timeout = default_timeout
        self.long_running_approved: bool = False
        self.session_timeout: Optional[int] = None
        self.approval_metadata: dict = {}

    def request_long_running_approval(self, estimated_minutes: float) -> bool:
        """Request approval for long-running experiment.

        If already approved this session, returns True immediately without prompting.
        Otherwise, displays estimated duration and grants approval automatically
        (designed for agent context, not interactive use).

        Args:
            estimated_minutes: Estimated experiment duration in minutes

        Returns:
            True if approval granted, False if declined

        Example:
            >>> tm = ExperimentTimeoutManager()
            >>> approved = tm.request_long_running_approval(45)
            >>> print(f"Approved: {approved}")
        """
        # If already approved, return immediately
        if self.long_running_approved:
            return True

        # Print warning about long-running experiment
        print(f"\n{'='*70}")
        print(f"LONG-RUNNING EXPERIMENT DETECTED")
        print(f"{'='*70}")
        print(f"Estimated duration: {estimated_minutes:.1f} minutes")
        print(f"Standard timeout: {self.default_timeout / 60:.1f} minutes")
        print(f"\nThis experiment exceeds the standard task timeout.")
        print(f"Granting approval for long-running mode (session-level).")
        print(f"{'='*70}\n")

        # Grant approval automatically (for agent context)
        self.long_running_approved = True
        self.session_timeout = None  # No timeout

        # Log approval in metadata for audit trail
        self.approval_metadata = {
            "timestamp": datetime.utcnow().isoformat(),
            "estimated_minutes": estimated_minutes,
            "granted": True,
            "reason": "long_running_experiment",
        }

        return True

    def get_timeout(self, estimated_seconds: float) -> Optional[int]:
        """Get appropriate timeout value based on estimate and approval state.

        Args:
            estimated_seconds: Estimated experiment duration in seconds

        Returns:
            Timeout in seconds, or None for no timeout

        Rules:
            - If estimated_seconds <= 600: return default_timeout
            - If long_running_approved: return None (no timeout)
            - Otherwise: return default_timeout

        Example:
            >>> tm = ExperimentTimeoutManager()
            >>> tm.get_timeout(300)  # Short experiment
            600
            >>> tm.request_long_running_approval(30)
            >>> tm.get_timeout(3600)  # Long experiment after approval
            None
        """
        # Short experiments always use default timeout
        if estimated_seconds <= self.default_timeout:
            return self.default_timeout

        # Long experiments after approval have no timeout
        if self.long_running_approved:
            return None

        # Long experiments without approval use default timeout (will likely fail)
        return self.default_timeout

    def reset_approval(self) -> None:
        """Reset approval state to default.

        Clears the long-running approval flag and session timeout.
        Useful when starting a new session or after an experiment completes.

        Example:
            >>> tm = ExperimentTimeoutManager()
            >>> tm.request_long_running_approval(30)
            >>> tm.long_running_approved
            True
            >>> tm.reset_approval()
            >>> tm.long_running_approved
            False
        """
        self.long_running_approved = False
        self.session_timeout = None
        self.approval_metadata = {}

    def get_approval_metadata(self) -> dict:
        """Get audit trail of approval events.

        Returns:
            Dictionary containing approval metadata:
            - timestamp: When approval was granted (ISO format)
            - estimated_minutes: Estimated duration at approval time
            - granted: Whether approval was granted
            - reason: Why approval was needed

        Example:
            >>> tm = ExperimentTimeoutManager()
            >>> tm.request_long_running_approval(45)
            >>> metadata = tm.get_approval_metadata()
            >>> print(metadata["estimated_minutes"])
            45
        """
        return self.approval_metadata.copy()
