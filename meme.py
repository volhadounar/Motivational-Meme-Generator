import os
import random
import argparse

from MemeEngine.meme_engine import MemeEngine
from QuoteEngine.ingestor import Ingestor
from QuoteEngine.models import QuoteModel
from constants import QUOTE_FILES, IMAGE_SOURCE_PATH


def generate_meme(path=None, body=None, author=None):
    """ Generate a meme given an path and a quote """
    img = None
    quote = None

    if path is None:
        imgs = []
        for root, dirs, files in os.walk(IMAGE_SOURCE_PATH):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path[0]

    if body is None:
        quotes = []
        for file in QUOTE_FILES:
            quotes.extend(Ingestor.parse(file))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    meme = MemeEngine('./tmp')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate meme with quote')
    parser.add_argument('--path', type=str, default=None, help='Provide the source image path')
    parser.add_argument('--body', type=str, default=None, help='Provide the text to be printed on the image')
    parser.add_argument('--author', type=str, default=None, help='Provide the author of the quote')
    args = parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))

