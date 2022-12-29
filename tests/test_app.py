import unittest
import io
from flask import Flask
from app import app
from PIL import Image
from unittest.mock import patch, MagicMock
import pathlib

class TestApp(unittest.TestCase):

    @staticmethod
    def get_image_file(size=(50, 50),
                       color=(256, 0, 0)) -> io.BytesIO:
        file_obj = io.BytesIO()
        image = Image.new('RGB', size=size, color=color)
        image.save(file_obj, 'png')
        file_obj.seek(0)
        return file_obj.read()

    @patch('app.meme')
    def test_meme_rand(self, mock):
        with app.test_client() as client:
            mock.make_meme.return_value = './static/61146707.jpg'
            response = client.get('/')
            data = response.data.decode()
            assert response.status_code in (200,)
            assert './static/61146707.jpg' in data

    @patch('app.requests.get')
    @patch('MemeEngine.meme_engine.random.randint')
    def test_meme_post(self, mock_random, mock_request):
        with app.test_client() as client:
            mock_response = MagicMock()
            mock_response.content = self.get_image_file()
            mock_request.return_value = mock_response
            mock_random.return_value = 1234
            response = client.post('/create', data = {
                'image_url': 'https://ttt.com',
                'body': 'body',
                'author': 'author'
            })
            data = response.data.decode()
            assert response.status_code in (200,)
            assert './static/1234.jpg' in data
