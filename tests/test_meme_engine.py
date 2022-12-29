from PIL import Image
import unittest
import pathlib
import os

from MemeEngine.meme_engine import MemeEngine

                           
class TestMemeEngine(unittest.TestCase):
    def test_make_meme(self):
        image_path = pathlib.Path(__file__).parent.resolve() / 'utils/' / 'test_image.jpg'
        path = MemeEngine('./tmp').make_meme(image_path, 'You must be the change you wish to see in the world', 'Gandhi')
        with Image.open(path) as image:
            self.assertEqual(image.size, (500, 500))
        os.remove(path)
        
    def test_wrong_source_file(self):
        image_path = pathlib.Path(__file__).parent.resolve() / 'test_image.jpg'
        with self.assertRaises(FileNotFoundError):
            MemeEngine('./tmp').make_meme(image_path, '', '')
