import os
import shutil

CATEGORY_TO_FOLDER = {
    "image_general": "Images",
    "archive": "Archives",
    "executable": "Executables",
    "text_notes": "Docs/Notes",
    "text_document": "Docs/Documents"
}

CONFIDENCE_THRESHOLD = 0.6


def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def move_file(file_path, base_dir, category, confidence):
    if confidence < CONFIDENCE_THRESHOLD or category not in CATEGORY_TO_FOLDER:
        target_dir = os.path.join(base_dir, "Unsorted")
    else:
        target_dir = os.path.join(base_dir, CATEGORY_TO_FOLDER[category])

    ensure_folder(target_dir)

    file_name = os.path.basename(file_path)
    target_path = os.path.join(target_dir, file_name)

    shutil.move(file_path, target_path)

    print(f"Moved → {file_name} → {target_dir}")
