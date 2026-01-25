import folder_manager
import os

print("Inspecting CATEGORY_TO_FOLDER values for hidden characters:")
for key, value in folder_manager.CATEGORY_TO_FOLDER.items():
    print(f"Key: '{key}', Value: '{value}', Repr: {repr(value)}")

print("\nListing directories in destination to check for duplicates:")
# Using the path from your main.py
base_dir = r"C:\Users\Himanshu\Downloads\sorted"
if os.path.exists(base_dir):
    for name in os.listdir(base_dir):
        print(f"Name: '{name}', Repr: {repr(name)}")
else:
    print(f"Directory {base_dir} does not exist.")
