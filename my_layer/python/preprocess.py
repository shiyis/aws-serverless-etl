import pandas as pd
import re
import unicodedata
import contractions

pd.set_option('display.min_rows', 50)
pd.options.display.max_colwidth = 150

def standardize_accented_chars(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

def remove_urls(text):
    return re.sub(r'http\S+','', text)

def expand_contractions(text):
    expanded_words = []
    for word in text.split():
        expanded_words.append(contractions.fix(word))
    return ' '.join(expanded_words)

def remove_mentions_and_tags(text):
    text = re.sub(r'@\S*', '', text)
    text = re.sub(r'&\S*', '', text)
    return re.sub(r'#\S*', '', text)



def preprocess(text):
    text = remove_mentions_and_tags(text)
    text = expand_contractions(text)
    text = remove_urls(text)
    return text


def df_apply(event):
    df = pd.read_csv(event['dir'] + "out.csv")
    df['text'] = df['text'].apply(preprocess)
    # df.to_csv(event['dir']+"out_preprocessed.csv")
    try:
        return df.loc[0,'text']
    except ValueError:
        print('no data')
    return df
