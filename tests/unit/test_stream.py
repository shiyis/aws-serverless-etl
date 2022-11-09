from functions.filtered_stream import app
from time import time
import os
import unittest
import json

class TestStringMethods(unittest.TestCase):
    def test_stream(self):
        data = app.lambda_handler("","")
        data = json.loads(list(data.values())[1])
        assert len(data["message"][0][0])== len("1584695563609870336")