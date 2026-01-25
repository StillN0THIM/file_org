# main.py

import os
from category_decider import decide_category
from folder_manager import move_file

BASE_DIR = r"C:\Users\Himanshu\Downloads\sorted"
INPUT_DIR = r"C:\Users\Himanshu\Downloads"

for file_name in os.listdir(INPUT_DIR):
    file_path = os.path.join(INPUT_DIR, file_name)

    if os.path.isfile(file_path):
        category, confidence = decide_category(file_path)
        move_file(file_path, BASE_DIR, category, confidence)
