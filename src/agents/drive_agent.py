from src.tools.drive_real import DriveTool
from src.tools.llm_stub import LLMStub
from src.agents.agent_base import AgentBase

class DriveAgent(AgentBase):
    def __init__(self, drive_tool: DriveTool, llm: LLMStub):
        super().__init__("DriveAgent")
        self.drive = drive_tool
        self.llm = llm

    def fetch_and_summarize(self, folder_id=None):
        # same behavior, return list of dicts
        files = self.drive.list_docs(folder_id)
        results = []
        for f in files:
            file_id = f["id"]
            text = self.drive.download_text(file_id)
            summary = self.llm.summarize(text)
            tasks = self.llm.extract_tasks(text)
            results.append({"file": f["name"], "summary": summary, "tasks": tasks})
        return results

    def handle_message(self, msg):
        # simple example: if asked to fetch, perform action
        payload = msg.get("payload", {})
        if payload.get("cmd") == "fetch":
            folder = payload.get("folder_id")
            data = self.fetch_and_summarize(folder)
            # reply via A2A is done by coordinator
            print(f"[DriveAgent] fetched {len(data)} docs")
