from PIL import Image, ExifTags
import os


def image_meta_sort(file_path):
    try:
        img = Image.open(file_path)
        width, height = img.size
        format = img.format
        exif_data = extract_exif(img)

        # 📸 Camera photos
        if "Model" in exif_data:
            return "image_camera", 0.95

        # 🖼 Screenshots (heuristic)
        if is_screenshot(width, height):
            return "image_screenshot", 0.85

        # 🎨 Generated / design tools
        if "Software" in exif_data:
            software = exif_data["Software"].lower()
            if any(x in software for x in ["figma", "canva", "photoshop"]):
                return "image_generated", 0.90

        return "image_general", 0.70

    except Exception:
        return "image_unknown", 0.40


def extract_exif(img):
    exif_raw = img._getexif()
    if not exif_raw:
        return {}

    return {
        ExifTags.TAGS.get(k, k): v
        for k, v in exif_raw.items()
    }


def is_screenshot(w, h):
    common_resolutions = [
        (1920, 1080),
        (1366, 768),
        (1284, 2778),
        (1170, 2532)
    ]
    return (w, h) in common_resolutions
