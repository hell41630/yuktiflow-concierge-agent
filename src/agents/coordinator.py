import threading
from typing import List, Dict, Any, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.observability.logger import log_event

class Coordinator:
    """
    Orchestrates agents:
    - run_sequential(list_of_callables)
    - run_parallel(list_of_callables)
    - start_loop_agent(agent, interval, max_iter)
    - send_a2a(sender, receiver, payload)
    """

    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=6)
        self.metrics = None

    def run_sequential(self, steps: List[Callable[[], Any]]):
        """Run callables one after the other; log start/finish."""
        results = []
        for i, fn in enumerate(steps):
            log_event("Coordinator", "step_start", {"index": i, "fn": getattr(fn, "__name__", str(fn))})
            res = fn()
            log_event("Coordinator", "step_done", {"index": i, "result_summary": str(type(res))})
            results.append(res)
        return results

    def run_parallel(self, tasks: List[Callable[[], Any]]):
        futures = {self.executor.submit(t): t for t in tasks}
        results = []
        for fut in as_completed(futures):
            try:
                results.append(fut.result())
            except Exception as e:
                log_event("Coordinator", "parallel_task_error", {"error": str(e)})
        return results

    def start_loop_agent(self, agent, interval_seconds=5.0, max_iterations=5):
        agent.start_loop(interval_seconds=interval_seconds, max_iterations=max_iterations)
        log_event("Coordinator", "started_loop_agent", {"agent": agent.name})

    def send_a2a(self, sender_name: str, receiver, payload: Dict[str, Any]):
        from src.observability.metrics import Metrics

        # Create metrics tracker if not exists
        if self.metrics is None:
            self.metrics = Metrics()
            self.metrics.mark_start()

        # Count the A2A message
        self.metrics.inc("a2a_messages", 1)

        # Log event
        log_event("Coordinator", "a2a_send", {
            "from": sender_name,
            "to": receiver.name,
            "payload": payload
        })

        # Deliver the message to the target agent
        receiver.send_message({"from": sender_name, "payload": payload})
