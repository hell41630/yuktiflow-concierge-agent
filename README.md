📘 YuktiFlow – AI-Powered Concierge Task Orchestration System

YuktiFlow (युक्ति + Flow) combines the Sanskrit word Yukti—“strategy, intelligent solution”—with the idea of seamless workflow automation.
It is a multi-agent AI system designed to automatically extract tasks from your real documents, plan them intelligently, schedule them, and track execution — all without manual intervention.

🌟 1. Overview

YuktiFlow is an AI Concierge Agent that reads meeting notes, emails, or documents from Google Drive, extracts action items, plans & prioritizes them, schedules them, and stores progress over time.

It implements all major concepts taught in Google’s 5-Day AI Agents Intensive Course, including:

Multi-Agent System

LLM-Driven Agents (Gemini)

Sequential + Parallel + Loop Agents

A2A Communication Protocol

Tool Use (Google Drive API + Gemini API)

Memory Bank (long-term JSON state storage)

Context Compaction Agent

Observability (Logging, Metrics, Tracing)

Clean Architecture & Modularity

🎯 2. Problem Statement

Managing daily tasks hidden inside documents (meeting notes, emails, reports) is:

Time-consuming

Error-prone

Mentally taxing

Easy to forget

Users want an automatic system that reads documents, extracts tasks, plans them, schedules them, and tracks progress — just like a personal assistant.

🤖 3. Solution Summary

YuktiFlow is a fully automated pipeline:

1️⃣ DriveAgent – Fetches Google Docs files and extracts their text
2️⃣ GeminiLLM – Summarizes and extracts tasks
3️⃣ PlannerAgent – Prioritizes and expands tasks (A2A → Scheduler & Compactor)
4️⃣ ContextCompactorAgent – Compresses context into short summaries
5️⃣ SchedulerAgent – Auto-assigns timestamps
6️⃣ TrackerAgent – Stores schedules and tracks iterations
7️⃣ Coordinator – Manages sequencing, parallel tasks & A2A messages
8️⃣ MemoryBank – Saves all progress to memory.json
9️⃣ Metrics – Saves observability to metrics.json

The user simply drops a file in Google Drive → The system handles everything else.

🏗️ 4. Architecture Diagram
               ┌──────────────────┐
               │   Google Drive    │
               └─────────┬────────┘
                         ▼
                ┌──────────────────┐
                │   DriveAgent      │
                └─────────┬────────┘
                          ▼
                ┌──────────────────┐
                │ Gemini LLM Tools │
                └─────────┬────────┘
                          ▼
                ┌──────────────────────────┐
                │      PlannerAgent        │
                └────────┬──────┬──────────┘
                         │      │
              A2A(plan)  │      │ A2A(compact)
                         ▼      ▼
             ┌──────────────┐ ┌──────────────────┐
             │ SchedulerAgent│ │ContextCompactor  │
             └──────┬────────┘ └──────────┬──────┘
                    │ A2A(schedule)        │
                    ▼                       │
            ┌──────────────────┐            │
            │  TrackerAgent    │◄───────────┘
            └──────┬──────────┘
                   ▼
          ┌──────────────────┐
          │   MemoryBank     │
          └──────────────────┘

🧩 5. Key Features
✔ Multi-Agent System

DriveAgent (sequential)

PlannerAgent (LLM A2A agent)

SchedulerAgent (parallel)

TrackerAgent (loop agent)

ContextCompactorAgent (LLM summarizer)

✔ A2A Communication

Agents send messages like:

{"cmd": "plan", "tasks": [...]}

✔ Observability

Logging → logs/events.log

Metrics → metrics.json

Agent lifecycle traces

✔ Long-Term Memory

memory.json stores:

previous summaries

schedules

tracker iterations

🧠 6. Setup Instructions
Clone the repo
git clone https://github.com/hell41630/yuktiflow-concierge-agent.git
cd yuktiflow-concierge-agent

Install dependencies
pip install -r requirements.txt

Insert secrets (NOT COMMITTED)

Add:

secrets/gemini_key.txt
secrets/service_account.json

Run the agent pipeline
python -m src.main

📄 7. Project Folder Structure
src/
 ├─ agents/
 │   ├─ drive_agent.py
 │   ├─ planner_agent.py
 │   ├─ scheduler_agent.py
 │   ├─ tracker_agent.py
 │   ├─ context_compactor_agent.py
 │   └─ coordinator.py
 ├─ tools/
 │   ├─ llm_gemini.py
 │   └─ drive_real.py
 ├─ memory/
 │   └─ memory_bank.py
 ├─ observability/
 │   ├─ logger.py
 │   └─ metrics.py
 └─ main.py

🏁 8. Running Example Output
MAIN.PY IS RUNNING (coordinator mode)
[DriveAgent] Docs fetched: 2
[PlannerAgent] A2A: planned 4 tasks
[SchedulerAgent] scheduled 4 tasks
[TrackerAgent] stored schedule
Done. Check memory.json and metrics.json for results.

🪄 9. Why YuktiFlow?

Yukti (युक्ति) = strategy, intelligence, clever solution
Flow = smooth automated process

Together → An intelligent system that automates your life.

🔗 10. Links

GitHub Repo:
https://github.com/hell41630/yuktiflow-concierge-agent
