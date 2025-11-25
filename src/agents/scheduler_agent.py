from src.agents.agent_base import AgentBase
import datetime

class SchedulerAgent(AgentBase):
    def __init__(self):
        super().__init__("SchedulerAgent")
        self.coordinator = None
        self.tracker = None

    def handle_message(self, msg):
        payload = msg.get("payload", {})
        if payload.get("cmd") != "schedule":
            return

        tasks = payload.get("tasks", [])

        schedule = []
        base = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)

        for i, t in enumerate(tasks):
            schedule.append({
                "task": t["task"],
                "time": (base + datetime.timedelta(minutes=30 * i)).isoformat()
            })

        print(f"[SchedulerAgent] scheduled {len(schedule)} tasks")

        # Send to tracker for saving
        if self.tracker and self.coordinator:
            self.coordinator.send_a2a(
                sender_name="SchedulerAgent",
                receiver=self.tracker,
                payload={"cmd": "store_schedule", "schedule": schedule}
            )
