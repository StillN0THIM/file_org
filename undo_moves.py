import os
import shutil

LOG_FILE = "move_log.txt"

def log_move(src, dst):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{src}|||{dst}\n")

def undo_moves():
    if not os.path.exists(LOG_FILE):
        print("No moves to undo.")
        return

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Undo in reverse order
    for line in reversed(lines):
        src, dst = line.strip().split("|||")
        if os.path.exists(dst):
            os.makedirs(os.path.dirname(src), exist_ok=True)
            shutil.move(dst, src)

    os.remove(LOG_FILE)
    print("Undo completed successfully.")
