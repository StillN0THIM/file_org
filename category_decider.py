# category_decider.py

def decide_category(file_path):
    """
    Returns:
        category_label (str)
        confidence (float between 0 and 1)
    """

    ext = file_path.lower().split('.')[-1]

    if ext in ["jpg", "png", "jpeg"]:
        return "image_general", 0.95

    if ext in ["zip", "rar"]:
        return "archive", 0.98

    if ext in ["exe"]:
        return "executable", 0.99

    if ext in ["txt", "md","pdf"]:
        return "text_notes", 0.72

    return "unknown", 0.30
