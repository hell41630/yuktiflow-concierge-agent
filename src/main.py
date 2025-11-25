from src.agents.context_compactor_agent import ContextCompactorAgent

print("MAIN.PY IS RUNNING (coordinator mode)")
from src.observability.metrics import Metrics
from src.agents.context_compactor_agent import ContextCompactorAgent

from src.tools.drive_real import DriveTool
from src.tools.llm_gemini import GeminiLLM
from src.memory.memory_bank import MemoryBank
from src.agents.drive_agent import DriveAgent
from src.agents.planner_agent import PlannerAgent
from src.agents.scheduler_agent import SchedulerAgent
from src.agents.tracker_agent import TrackerAgent
from src.agents.coordinator import Coordinator
from src.observability.logger import log_event
import time
import json

def run_pipeline():
    # Start metrics
    metrics = Metrics()
    metrics.mark_start()

    # init tools
    drive = DriveTool()
    with open("secrets/gemini_key.txt") as f:
        GEMINI_KEY = f.read().strip()
    llm = GeminiLLM(GEMINI_KEY)
    memory = MemoryBank("memory.json")

    # init agents
    drive_agent = DriveAgent(drive, llm)
    planner = PlannerAgent(memory)
    scheduler = SchedulerAgent()
    tracker = TrackerAgent(memory)
    compactor = ContextCompactorAgent(llm, memory)


    coord = Coordinator()

    # Link agents for A2A
    planner.coordinator = coord
    planner.scheduler = scheduler
    scheduler.coordinator = coord
    scheduler.tracker = tracker
    planner.compactor = compactor
    compactor.coordinator = coord


    # STEP 1 — Fetch docs (sequential)
    def step_fetch():
        return drive_agent.fetch_and_summarize(FOLDER_ID)

    docs = coord.run_sequential([step_fetch])[0]

    # metrics: docs
    metrics.set("docs_fetched", len(docs))

    # Extract tasks from docs
    all_tasks = [task for doc in docs for task in doc["tasks"]]

    # metrics: tasks extracted
    metrics.set("tasks_extracted", len(all_tasks))

    # STEP 2 — A2A: ask PlannerAgent to plan tasks
    coord.send_a2a(
        sender_name="Main",
        receiver=planner,
        payload={"cmd": "plan", "tasks": all_tasks}
    )

    # allow time for A2A planning & scheduling
    time.sleep(2)

    # STEP 3 — Start Tracker loop agent
    coord.start_loop_agent(tracker, interval_seconds=2, max_iterations=4)

    # Wait for tracker loop
    time.sleep(8)

    # Read memory to get tracker iterations
    tracker_data = memory.load()
    metrics.set("tracker_iterations", tracker_data.get("tracker_runs", 0))

    # End metrics
    metrics.mark_end()
    metrics.save()

    print("\nDone. Check memory.json and metrics.json for results.")

# your Google Drive folder ID
FOLDER_ID = "10UxgvGGxkktUXhq6PY-uNRpFETCG8Rbl"

if __name__ == "__main__":
    run_pipeline()
