import time
import json

def log_event(agent, action, details):
    event = {
        "time": time.time(),
        "agent": agent,
        "action": action,
        "details": details
    }
    print(json.dumps(event))
