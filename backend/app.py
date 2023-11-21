"""
This module implements a simple web application using Flask. The application
allows users to upload images, which are then automatically watermarked. The
processed images are stored in an output directory and returned to the user
for download.

The watermarking is done using the PIL (Python Imaging Library). The Flask
server handles both image uploading and the delivery of processed images.
The upload and output folders are automatically created if they don't exist.

Routes:
- `/`: Displays the main page and handles image uploads and downloads.

Functions:
- `index()`: Route to render the main page and handle image upload requests.
- `add_watermark(input_image_path, output_image_name)`: Adds a watermark to
  the uploaded image and saves the processed image.
"""

import os

from flask import Flask, request, send_from_directory, abort
from PIL import Image
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config.from_pyfile("config.py")

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["OUTPUT_FOLDER"], exist_ok=True)


@app.route("/", methods=["POST"])
def index():
    """
    Handle POST request for image upload and watermarking.

    Processes uploaded file, adds watermark, and returns
    it. Logs errors and sends a 500 response on failure.

    Returns:
        Watermarked image for download or HTTP 500 on error.
    """
    if request.method == "POST":
        file = request.files.get("file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            try:
                add_watermark(filepath, filename)
                return send_from_directory(
                    app.config["OUTPUT_FOLDER"], filename, as_attachment=True
                )
            except (IOError, OSError) as e:
                app.logger.error("Error processing the image: %s", e)
                abort(500)
            except Exception as e:  # Catch other unforeseen exceptions
                app.logger.error("Unexpected error: %s", e)
                abort(500)


def add_watermark(input_image_path, output_image_name):
    """
    Add watermark to the uploaded image.

    Opens uploaded image and watermark image, combines
    them, and saves the watermarked image in output directory.

    Args:
        input_image_path (str): Path of uploaded image.
        output_image_name (str): Name for the watermarked file.

    Returns:
        None. Saves watermarked image to file system.
    """
    try:
        original = Image.open(input_image_path).convert("RGBA")
        watermark = Image.open(app.config["WATERMARK_PATH"]).convert("RGBA")

        # Calculate the proportions to resize the watermark
        aspect_ratio = watermark.width / watermark.height
        new_width = int(original.width * 0.2)
        new_height = int(new_width / aspect_ratio)

        watermark = watermark.resize((new_width, new_height))

        transparent = Image.new("RGBA", original.size, (255, 255, 255, 0))
        transparent.paste(original, (0, 0), mask=original)
        transparent.paste(
            watermark,
            (
                original.size[0] - watermark.size[0] - 10,
                original.size[1] - watermark.size[1] - 10,
            ),
            mask=watermark,
        )

        watermarked_filename = os.path.join(
            app.config["OUTPUT_FOLDER"], output_image_name
        )
        transparent.save(watermarked_filename, "PNG")
    finally:
        original.close()
        watermark.close()


def allowed_file(filename):
    """
    Check if file extension is allowed.

    Args:
        filename (str): Uploaded file name.

    Returns:
        bool: True if extension is allowed, else False.
    """
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


if __name__ == "__main__":
    debug_mode = bool(int(os.environ.get("FLASK_DEBUG", 1)))
    app.run(debug=debug_mode)
