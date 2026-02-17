import json
from pathlib import Path

DATA_FILE = Path("data.json")

def init_db():
    if not DATA_FILE.exists():
        DATA_FILE.write_text(json.dumps({"classes": [], "students": []}, indent=4), encoding="utf-8")

def read_db():
    init_db()
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))

def write_db(data):
    DATA_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")
