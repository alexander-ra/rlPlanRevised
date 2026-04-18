"""Logging utilities for Step 03."""

import os
import json
from datetime import datetime


class TrainingLogger:
    """Simple JSON-based training logger."""

    def __init__(self, log_dir: str, run_name: str = "cfr"):
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_path = os.path.join(log_dir, f"{run_name}_{timestamp}.json")
        self.entries = []

    def log(self, iteration: int, **kwargs):
        entry = {"iteration": iteration, **kwargs}
        self.entries.append(entry)

    def save(self):
        with open(self.log_path, "w") as f:
            json.dump(self.entries, f, indent=2)
        print(f"  Log saved to: {self.log_path}")
