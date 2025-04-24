import os

import pillow_heif
from PIL import Image

pillow_heif.register_heif_opener()

# Configurable max dimension (in pixels) for width or height
MAX_DIMENSION = 1200
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".heic"}


def resize_image(path):
    try:
        with Image.open(path) as img:
            img_format = img.format
            original_ext = os.path.splitext(path)[1].lower()
            width, height = img.size

            # Skip images that are already small enough
            if max(width, height) <= MAX_DIMENSION:
                return

            # Compute new size
            if width > height:
                new_width = MAX_DIMENSION
                new_height = int((MAX_DIMENSION / width) * height)
            else:
                new_height = MAX_DIMENSION
                new_width = int((MAX_DIMENSION / height) * width)

            resized = img.resize((new_width, new_height), Image.LANCZOS)
            if original_ext == ".heic":
                new_path = os.path.splitext(path)[0] + ".jpg"
                resized = resized.convert("RGB")
                resized.save(new_path, format="JPEG", quality=85, optimize=True)
                os.remove(path)
                print(f"Converted and resized: {path} -> {new_path} ({width}x{height} -> {new_width}x{new_height})")
            else:
                resized.save(path, format="JPEG", quality=85, optimize=True)
                print(f"Resized: {path} ({width}x{height} -> {new_width}x{new_height})")

    except Exception as e:
        print(f"Error processing {path}: {e}")


def process_directory(base_path):
    for root, _, files in os.walk(base_path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                full_path = os.path.join(root, file)
                resize_image(full_path)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python resize_images.py /path/to/images")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print("Provided path is not a directory")
        sys.exit(1)

    process_directory(directory)
