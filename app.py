"""Main application module."""
import io
import random
import os
import requests
from flask import Flask, render_template, abort, request

from QuoteEngine.ingestor import Ingestor
from constants import QUOTE_FILES, IMAGE_SOURCE_PATH, IMAGE_DESTINATION_PATH
from MemeEngine.meme_engine import MemeEngine


def create_app(config_filename: str = __name__) -> Flask:
    """Set up the application."""
    return Flask(config_filename)

app = create_app()


meme = MemeEngine(IMAGE_DESTINATION_PATH)

def setup():
    """Load all resources."""
    quotes = []
    for file_path in QUOTE_FILES:
        quotes.extend(Ingestor.parse(file_path))

    imgs = []
    for root, _, files in os.walk(IMAGE_SOURCE_PATH):
        imgs = [os.path.join(root, name) for name in files]
    return quotes, imgs


quotes, images = setup()


@app.route('/')
def meme_rand():
    """Generate a random meme."""
    image = random.choice(images)
    quote = random.choice(quotes)
    path = meme.make_meme(image, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user defined meme by uploading source image using input url."""
    image_url = request.form['image_url']
    body = request.form['body']
    author = request.form['author']
    image = io.BytesIO(requests.get(image_url).content)
    path = meme.make_meme(image, body, author)
    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()