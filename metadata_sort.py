from PIL import Image
from PIL.ExifTags import TAGS
import piexif


def extract_image_metadata(image_path):
    metadata = {}

    # ---------- OPEN IMAGE ----------
    img = Image.open(image_path)

    # ---------- BASIC INFO ----------
    metadata["Filename"] = image_path
    metadata["Format"] = img.format
    metadata["Mode"] = img.mode
    metadata["Size"] = img.size  # (width, height)

    # ---------- EXIF DATA ----------
    exif_data = img._getexif()
    if exif_data:
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            metadata[tag_name] = value
    else:
        metadata["EXIF"] = None

    # ---------- DETAILED EXIF (PIEXIF) ----------
    try:
        exif_dict = piexif.load(image_path)
        for ifd in exif_dict:
            if isinstance(exif_dict[ifd], dict):
                for tag, value in exif_dict[ifd].items():
                    tag_name = piexif.TAGS[ifd][tag]["name"]
                    metadata[f"{ifd}:{tag_name}"] = value
    except Exception:
        metadata["PIEXIF"] = None

    return metadata


def detect_image_source(metadata):
    software = str(metadata.get("Software", "")).lower()

    if "canva" in software:
        return "Canva"
    if "figma" in software:
        return "Figma"
    if "photoshop" in software:
        return "Photoshop"
    if "gimp" in software:
        return "GIMP"
    if metadata.get("Make") and metadata.get("Model"):
        return "Camera"

    return "Unknown"


# ---------- USAGE ----------
image_path = r"C:\Users\Himanshu\Downloads\sorted\Images\4.jpeg"

meta = extract_image_metadata(image_path)
meta["ImageSource"] = detect_image_source(meta)

for key, value in meta.items():
    print(f"{key}: {value}")
