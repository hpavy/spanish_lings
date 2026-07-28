import json
import os

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "progress.json")


def load(path=DEFAULT_PATH):
    if not os.path.exists(path):
        return {"srs": {}, "unlocked_tiers": []}
    with open(path) as f:
        return json.load(f)


def save(data, path=DEFAULT_PATH):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=True)
