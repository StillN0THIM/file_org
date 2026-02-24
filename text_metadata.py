import os
import shutil
from collections import defaultdict
from undo_moves import log_move   

# ---------------- CONFIG ----------------
WORD_COUNT_TOL = 0.10
LINE_COUNT_TOL = 0.10
AVG_LINE_LEN_TOL = 0.10
RATIO_TOL = 0.05


# ---------------- METADATA ----------------
def extract_metadata(file_path):
    with open(file_path, "r", errors="ignore") as f:
        text = f.read()

    lines = text.splitlines()
    words = text.split()
    chars = len(text)

    if chars == 0:
        return None

    digits = sum(c.isdigit() for c in text)
    symbols = chars - digits - sum(c.isalpha() for c in text)

    return {
        "file": file_path,
        "name": os.path.basename(file_path),
        "word_count": len(words),
        "line_count": len(lines),
        "avg_line_len": sum(len(l) for l in lines) / len(lines) if lines else 0,
        "digit_ratio": digits / chars,
        "symbol_ratio": symbols / chars
    }
def normalize_name(name):
    name = os.path.splitext(name)[0].lower()
    return "".join(c for c in name if c.isalnum())

def name_similarity(a, b):
    na = normalize_name(a)
    nb = normalize_name(b)

    if not na or not nb:
        return 0

    common = os.path.commonprefix([na, nb])
    return len(common) / max(len(na), len(nb))

# ---------------- SIMILARITY ----------------
def similar(a, b):
    def within(x, y, tol):
        return abs(x - y) / max(x, y, 1) <= tol

    name_sim = name_similarity(a["name"], b["name"])

    # Name-first boost
    if name_sim >= 0.05:   # filenames clearly related
        return (
            within(a["word_count"], b["word_count"], WORD_COUNT_TOL * 1.5) and
            within(a["line_count"], b["line_count"], LINE_COUNT_TOL * 1.5)
        )

    # Otherwise fall back to strict metadata match
    return (
        within(a["word_count"], b["word_count"], WORD_COUNT_TOL) and
        within(a["line_count"], b["line_count"], LINE_COUNT_TOL) and
        within(a["avg_line_len"], b["avg_line_len"], AVG_LINE_LEN_TOL) and
        within(a["digit_ratio"], b["digit_ratio"], RATIO_TOL)
    )

# ---------------- FOLDER NAME ----------------
def common_prefix(names):
    if len(names) == 1:
        return os.path.splitext(names[0])[0]

    prefix = os.path.commonprefix(names).rstrip("_- .")
    return prefix if len(prefix) >= 3 else names[0].split(".")[0]

# ---------------- GROUPING ----------------
def group_files(metadata_list):
    groups = []

    for meta in metadata_list:
        for group in groups:
            if similar(meta, group[0]):
                group.append(meta)
                break
        else:
            groups.append([meta])

    return groups



# ---------------- MAIN ----------------
def group_and_sort(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    metadata = []
    for file in os.listdir(input_dir):
        path = os.path.join(input_dir, file)
        if os.path.isfile(path):
            meta = extract_metadata(path)
            if meta:
                metadata.append(meta)

    groups = group_files(metadata)

    for group in groups:
        folder_name = common_prefix([m["name"] for m in group])
        folder_path = os.path.join(output_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        for m in group:
            dst = os.path.join(folder_path, m["name"])
            log_move(m["file"], dst)   # 👈 log before move
            shutil.move(m["file"], dst)

# ---------------- RUN ----------------
if __name__ == "__main__":
    INPUT_FOLDER  = r"C:\Users\Himanshu\Downloads\sorted\Docs\Notes"
    OUTPUT_FOLDER = r"C:\Users\Himanshu\Downloads\sorted\Docs\Notes_Sorted"


    group_and_sort(INPUT_FOLDER, OUTPUT_FOLDER)
