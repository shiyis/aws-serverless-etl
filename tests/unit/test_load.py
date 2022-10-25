from functions.load_data import app
import unittest

class TestStringMethods(unittest.TestCase):
    def test_data_loader(self):
        data = app.lambda_handler("", "")  
        assert "http" in data