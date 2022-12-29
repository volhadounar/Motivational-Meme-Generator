"""Provide class MemeEngine for.

Loading of a file from disk
Transform image by resizing to a maximum width of 500px while maintaining the input aspect ratio
Add a caption to an image (string input) with a body and author to a random location on the image.
Save the result to the provided output diractory.
"""
from PIL import Image, ImageDraw, ImageFont
import random
import logging

class MemeEngine:
    """Provide image operations for making a meme."""

    def __init__(self, outputdir):
        """Construct a new `MemeEngine` from outputdir.
        
        :out_path {str}: the desired location for the output image.
        """
        self.out_path = outputdir
        
    def make_meme(self, img_path, text, author, width=500) -> str:
        """Create a meme file With a Text from source image that is alocated by 'img_path' address.
        
        :in_path {str}: the file location for the input image.
        :text {str}: the text to put on the image.
        :author {str}: the author of the quote to put on image.
        :width {int}: The pixel width value. Default=500.
        :return {str}: the file path to the output image.
        """
        new_file_name = self.out_path + f'/{random.randint(0,100000000)}.jpg'
        try:
            with Image.open(img_path) as image:
                ratio = width/float(image.size[0])
                height = int(ratio*float(image.size[1]))
                image = image.resize((width, height), Image.NEAREST)
                draw = ImageDraw.Draw(image)
                fnt = ImageFont.truetype('./fonts/LilitaOne-Regular.ttf', size=15)
                text_to_draw = text + '. ' + author
                draw.text((40, 40), text_to_draw, font=fnt, fill=(255, 255, 255, 255))
                image.convert('RGB').save(new_file_name)
        except FileNotFoundError:
            logging.error(f'Cannot open file {new_file_name}')
            raise FileNotFoundError(f'Cannot open file {new_file_name}')
        return new_file_name
