from functions.load_data import app
import unittest

class TestStringMethods(unittest.TestCase):
    def test_data_loader(self):
        data = app.lambda_handler(None, "")
        assert 0 <= data["stock_price"] > 0 <= 100
