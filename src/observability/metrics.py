import json
import time
import os

class Metrics:
    def __init__(self, filename="metrics.json"):
        self.filename = filename
        self.data = {
            "run_start": None,
            "run_end": None,
            "duration_ms": None,
            "docs_fetched": 0,
            "tasks_extracted": 0,
            "tasks_planned": 0,
            "tasks_scheduled": 0,
            "tracker_iterations": 0,
            "a2a_messages": 0
        }

    def mark_start(self):
        self.data["run_start"] = time.time()

    def mark_end(self):
        self.data["run_end"] = time.time()
        self.data["duration_ms"] = int((self.data["run_end"] - self.data["run_start"]) * 1000)

    def inc(self, field, amt=1):
        if field in self.data:
            self.data[field] += amt

    def set(self, field, value):
        self.data[field] = value

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=2)
