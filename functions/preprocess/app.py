import unicodedata
import pandas as pd

import string
import re
import contractions
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
lemmatizer = WordNetLemmatizer()

#add punctuation char's to stopwords list
stop_words = stopwords.words('english')
stop_words += list(string.punctuation)
stop_words += ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'anxiety', 'rt']
stop_words += ["have","of","the","she","I",]

pd.set_option('display.min_rows', 50)
pd.options.display.max_colwidth = 150


def process_text(text):
    tokens = word_tokenize(text)
    stopwords_removed = [token.lower() for token in tokens if token.lower() not in stop_words]
    return stopwords_removed

def standardize_accented_chars(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

def remove_urls(text):
    return re.sub(r'http\S+','', text)

def expand_contractions(text):
    expanded_words = [] 
    for word in text.split():
        expanded_words.append(contractions.fix(word)) 
    return ' '.join(expanded_words)

def lemmatize_text(df_text):
    lemmatized =[]
    for w in df_text:
        lemmatized.append(lemmatizer.lemmatize(w))
    return lemmatized



def remove_mentions_and_tags(text):
    text = re.sub(r'@\S*', '', text)
    return re.sub(r'#\S*', '', text)


def keep_only_alphabet(text):
    return re.sub(r'[^a-z]', ' ', text)
    

def preprocess(df_text):
    text = remove_mentions_and_tags(text)
    text = keep_only_alphabet(text)
    text = remove_urls(text)
    tokens = word_tokenize(df_text)
    stopwords_removed = [token.lower() for token in tokens if token.lower() not in stop_words and len(token) > 3]

    lemmatized =[]

    for w in stopwords_removed:
        lemmatized.append(lemmatizer.lemmatize(w))

    processed = list(filter(lambda x: x.isalpha(), lemmatized))

    return processed

def lambda_handler(event, context):
    df = event.get("file")
    df['text'] = df['text'].apply(preprocess)
    return {"file":df}
