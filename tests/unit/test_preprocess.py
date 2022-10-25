from functions.preprocess import app
import unittest
import spacy
import string
import numpy as np
class TestStringMethods(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        stop_words = []
        stop_words += list(string.punctuation)
        stop_words += ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        stop_words += ["have","of","the","she","I","They","Her","She","Me","Something"]
        self.stop = set(stop_words)

    def test_remove_urls(self):
        assert app.remove_urls("https://www.google.com/") == ""
    
    def test_remove_stop(self):
        nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
        assert app.remove_stopwords("this is something fun!",nlp, self.stop) == "fun"
        assert app.remove_stopwords("this is something not fun!",nlp,self.stop) == "fun"
        assert app.remove_stopwords("I have done something wrong",nlp, self.stop) == "wrong"

    def test_expand_contractions(self):
        assert app.expand_contractions("i've") == "i have"

    def test_lemmatize_text(self):
        nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
        assert app.lemmatize("has had something lovey dovey cats",nlp) == "have have something lovey dovey cat"
 
    def test_remove_mentions_tags_retweets(self):
        assert app.remove_mentions_and_tags("@love") == ""
        assert app.remove_mentions_and_tags("#something") == ""

    def test_keep_only_alphabet(self):
        assert app.keep_only_alphabet("ajsdf123450") == "ajsdf"

    def test_standardize_accented_chars(self):
        assert app.standardize_accented_chars("é") == "e"

    def test_lambda_handler(self):
        assert type(app.lambda_handler("","")) == dict
        assert "text" in app.lambda_handler("","")["file"].columns
        assert type(app.lambda_handler("","")["file"].iloc[0,1]) == np.int64
        for i in ["@","#","http","rt"]:
            assert i not in app.lambda_handler("","")["file"].loc[0,"text"]

        