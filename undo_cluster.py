import os
import shutil
import json

LOG_FILE = "undo_log.json"

if not os.path.exists(LOG_FILE):
    print("No undo log found.")
    exit()

with open(LOG_FILE,
"r") as f:
    undo_log = json.load(f)

for moved_path, original_path in undo_log.items():
    os.makedirs(os.path.dirname(original_path), exist_ok=True)
    shutil.move(moved_path, original_path)
    print(f"Restored: {original_path}")

os.remove(LOG_FILE)
print("\nUndo completed.")