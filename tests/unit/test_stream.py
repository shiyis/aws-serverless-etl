from functions.filtered_stream import app
from time import time
import os
import unittest

class TestStringMethods(unittest.TestCase):
    def test_stream(self):
        data = app.lambda_handler("","")
        assert "text" in data[0]["data"]
        assert "id" in data[0]["data"]
        assert len(data[0]["data"]["id"]) == len("1584695563609870336")
        assert type(data[0]["data"]["text"]) == str
        assert os.path.isfile("./out.csv") 
