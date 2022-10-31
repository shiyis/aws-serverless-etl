import pandas as pd
import string
import re

#add punctuation char's to stopwords list
# custom_stop_words = stopwords.words('english')
# custom_stop_words += list(string.punctuation)
# custom_stop_words += list("1234567890")
# custom_stop_words += ["have","of","the","she","I","They","Her","She","Me","Something","RT"]
# custom_stop_words = set(custom_stop_words)
pd.set_option('display.min_rows', 50)
pd.options.display.max_colwidth = 150


def process_text(text):
    tokens = word_tokenize(text)
    stopwords_removed = [token.lower() for token in tokens if token.lower() not in custom_stop_words]
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

# def remove_stopwords(text,nlp,custom_stop_words=None, remove_small_tokens=True,min_len=2):
#     # if custom stop words are provided, then add them to default stop words list
#     if custom_stop_words:
#         nlp.Defaults.stop_words |= custom_stop_words

#     filtered_sentence =[]
#     doc=nlp(text)
#     for token in doc:

#         if token.is_stop == False:

#             # if small tokens have to be removed, then select only those which are longer than the min_len
#             if remove_small_tokens:
#                 if len(token.text)>min_len:
#                     filtered_sentence.append(token.text)
#             else:
#                 filtered_sentence.append(token.text)
#     # if after the stop word removal, words are still left in the sentence, then return the sentence as a string else return null
#     return " ".join(filtered_sentence) if len(filtered_sentence)> 0 else None

# def lemmatize(text, nlp):
#     doc = nlp(text)
#     lemmatized_text = []
#     for token in doc:
#         lemmatized_text.append(token.lemma_)
#     return " ".join(lemmatized_text)

def remove_mentions_and_tags(text):
    text = re.sub(r'@\S*', '', text)
    text = re.sub(r'&\S*', '', text)
    return re.sub(r'#\S*', '', text)



def preprocess(text):
    # nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
    text = remove_mentions_and_tags(text)
    text = expand_contractions(text)
    text = remove_urls(text)
    # tokens = word_tokenize(text)
    # print(tokens)
    # stopwords_removed = [token.lower() for token in tokens if token.lower() not in custom_stop_words and len(token) > 3]
    # stopwords_removed = remove_stopwords(text,nlp, custom_stop_words=custom_stop_words)
    # if stopwords_removed:
    #     lemmatized = lemmatize("".join(stopwords_removed),nlp).split()
    #     return " ".join(list(filter(lambda x: x.isalpha(), lemmatized))) if lemmatized else ""
    # else:
    #     return ""

    return text


def df_apply():
    df = pd.read_csv(context['dir'] + "out.csv")
    # print(df["text"])
    df['text'] = df['text'].apply(preprocess)
    # print(df["text"])
    df.to_csv(context['dir']+"out_preprocessed.csv")
    try:
        return df.loc[0,'text']
    except ValueError:
        print('no data')
