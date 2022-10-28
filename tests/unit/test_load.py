from functions.load_data import app
import unittest
import pytest
class TestStringMethods(unittest.TestCase):

    @pytest.mark.last
    def test_data_loader(self):
        context =  {'dir':'./output/'}
        data = app.lambda_handler("",context)
        assert "http" in data
