from src.agents.agent_base import AgentBase
import time

class PlannerAgent(AgentBase):
    def __init__(self, memory):
        super().__init__("PlannerAgent")
        self.memory = memory
        self.scheduler = None
        self.compactor = None

    def prioritize_and_expand(self, tasks, context_summary=None):
        """
        Simple planning logic:
        - wrap tasks as dicts
        - add default priority & estimates
        """
        planned = []
        for t in tasks:
            planned.append({
                "task": t,
                "priority_score": 1,
                "estimate_mins": 30
            })
        return planned

    def handle_message(self, msg):
        payload = msg.get("payload", {})

        if payload.get("cmd") == "plan":
            tasks = payload.get("tasks", [])
            plan = self.prioritize_and_expand(tasks)
            print(f"[PlannerAgent] A2A: planned {len(plan)} tasks")

            # Record metrics
            try:
                from src.observability.metrics import Metrics
                if not hasattr(self, "metrics"):
                    self.metrics = Metrics()
                self.metrics.set("tasks_planned", len(plan))
            except:
                pass

            # === A2A to ContextCompactorAgent ===
            if self.compactor and self.coordinator:
                self.coordinator.send_a2a(
                    sender_name="PlannerAgent",
                    receiver=self.compactor,
                    payload={"cmd": "compact", "tasks": plan}
                )
                print("[PlannerAgent] A2A sent to ContextCompactorAgent")

            # === A2A to SchedulerAgent ===
            if self.scheduler and self.coordinator:
                self.coordinator.send_a2a(
                    sender_name="PlannerAgent",
                    receiver=self.scheduler,
                    payload={"cmd": "schedule", "tasks": plan}
                )
                print("[PlannerAgent] A2A sent to SchedulerAgent")
