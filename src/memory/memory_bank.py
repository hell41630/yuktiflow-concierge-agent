import json
import os
from threading import Lock

class MemoryBank:
    def __init__(self, path):
        self.path = path
        self.lock = Lock()

        # Ensure file exists
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump({}, f)

    def load(self):
        with self.lock:
            with open(self.path, "r") as f:
                return json.load(f)

    def save(self, data):
        with self.lock:
            with open(self.path, "w") as f:
                json.dump(data, f, indent=2)

    # ⭐ REQUIRED: write(key, value)
    def write(self, key, value):
        data = self.load()
        data[key] = value
        self.save(data)

    # ⭐ Optional convenience read(key, default)
    def read(self, key, default=None):
        data = self.load()
        return data.get(key, default)
