import os

DEBUG = bool(int(os.environ.get("FLASK_DEBUG", 1)))
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
WATERMARK_PATH = "imagined-with-ai.png"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
