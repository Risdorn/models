import os
import random
from flask import Flask, render_template, send_from_directory, url_for
from pathlib import Path

app = Flask(__name__)
IMAGE_FOLDER = 'static/images'


def get_all_images(folder):
    """Recursively get all image file paths from folder."""
    exts = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
    return [str(p.relative_to('static')) for p in Path(folder).rglob('*') if p.suffix.lower() in exts]


def get_latest_image(folder):
    """Get the most recently modified image file."""
    all_images = [p for p in Path(folder).rglob('*') if p.suffix.lower() in ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')]
    if not all_images:
        return None
    latest = max(all_images, key=lambda p: p.stat().st_mtime)
    return str(latest.relative_to('static'))


@app.route('/')
def index():
    latest_image = get_latest_image(IMAGE_FOLDER)
    return render_template('index.html', image_path=latest_image)


@app.route('/random')
def random_image():
    all_images = get_all_images(IMAGE_FOLDER)
    if not all_images:
        return "No images found", 404
    return random.choice(all_images)


if __name__ == '__main__':
    # Use host='0.0.0.0' to make it accessible on the local LAN
    app.run(debug=True, host='0.0.0.0')