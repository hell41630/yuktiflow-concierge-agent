from src.agents.agent_base import AgentBase

class ContextCompactorAgent(AgentBase):
    def __init__(self, llm, memory):
        super().__init__("ContextCompactorAgent")
        self.llm = llm
        self.memory = memory
        self.coordinator = None

    def handle_message(self, msg):
        payload = msg.get("payload", {})

        if payload.get("cmd") != "compact":
            return

        tasks = payload.get("tasks", [])

        # Make compact text summary
        try:
            compact_text = self.llm.summarize(
                "Summarize these tasks for future reference:\n" +
                "\n".join([t["task"] for t in tasks])
            )
        except:
            compact_text = " ".join([t["task"] for t in tasks])

        # MemoryBank only supports write(key,value)
        self.memory.write("compact_context", compact_text)

        print("[ContextCompactorAgent] compacted & stored summary")
