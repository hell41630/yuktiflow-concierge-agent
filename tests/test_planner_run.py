# tests/test_planner_run.py
from src.agents.planner_agent import PlannerAgent
from src.memory.memory_bank import MemoryBank

# quick smoke test
mem = MemoryBank("memory.json")
planner = PlannerAgent(mem)

# simulate incoming A2A message
msg = {"from": "Main", "payload": {"cmd": "plan", "tasks": ["Task A", "Task B"]}}
planner.handle_message(msg)

print("Planner test done")
