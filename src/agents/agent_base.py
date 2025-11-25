import threading
import queue
from typing import Any, Dict, Optional
import time

class AgentBase:
    """
    Base class for all agents.
    Agents support:
      - Immediate A2A message handling (send_message)
      - Optional loop-based behavior (start_loop)
    """

    def __init__(self, name: str):
        self.name = name
        self.inbox = queue.Queue()
        self._running = False
        self.thread: Optional[threading.Thread] = None

    # ----------------------------
    # IMMEDIATE MESSAGE PROCESSING
    # ----------------------------
    def send_message(self, msg: Dict[str, Any]):
        """
        A2A messages are processed IMMEDIATELY.
        Also stored in inbox so loop agents can read if needed.
        """
        try:
            # Immediate
            self.handle_message(msg)
        except Exception as e:
            print(f"[{self.name}] Error in handle_message: {e}")

        # Optional: queue for loop processing
        self.inbox.put(msg)

    def handle_message(self, msg: Dict[str, Any]):
        """Must be implemented by child classes."""
        raise NotImplementedError

    # ----------------------------
    # LOOP AGENT SUPPORT
    # ----------------------------
    def start_loop(self, interval_seconds: float = 5.0, max_iterations: int = 5):
        """
        Used only by agents like TrackerAgent which need periodic work.
        """
        if self._running:
            return

        self._running = True

        def _run_loop():
            iterations = 0
            while self._running and (max_iterations is None or iterations < max_iterations):

                # Process inbox messages before each loop iteration
                while not self.inbox.empty():
                    msg = self.inbox.get()
                    try:
                        self.handle_message(msg)
                    finally:
                        self.inbox.task_done()

                # Call on_loop() if the agent implements it
                if hasattr(self, "on_loop"):
                    try:
                        self.on_loop()
                    except Exception as e:
                        print(f"[{self.name}] on_loop error: {e}")

                iterations += 1
                time.sleep(interval_seconds)

            self._running = False

        self.thread = threading.Thread(target=_run_loop, name=f"{self.name}-loop", daemon=True)
        self.thread.start()

    def stop_loop(self):
        """Stop the loop agent immediately."""
        self._running = False
        if self.thread:
            self.thread.join(timeout=2.0)
