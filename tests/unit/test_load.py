from functions.load_data import app
import unittest

class TestStringMethods(unittest.TestCase):
    def test_data_loader(self):
        context =  {'dir':'./output/'}
        data = app.lambda_handler("",context)  
        assert "http" in data