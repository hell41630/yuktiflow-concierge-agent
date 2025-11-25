from src.agents.agent_base import AgentBase

class TrackerAgent(AgentBase):
    def __init__(self, memory):
        super().__init__("TrackerAgent")
        self.memory = memory

    def handle_message(self, msg):
        payload = msg.get("payload", {})

        if payload.get("cmd") == "store_schedule":
            schedule = payload.get("schedule", [])
            self.memory.write("latest_schedule", schedule)
            print("[TrackerAgent] stored schedule")

    def on_loop(self):
        runs = self.memory.read("tracker_runs", 0)
        self.memory.write("tracker_runs", runs + 1)
        print(f"[TrackerAgent] loop #{runs + 1}")
