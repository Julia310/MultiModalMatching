import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords
import csv
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize


stemmer = SnowballStemmer("german")
stop_words = set(stopwords.words("german"))


def replace_specific_letters(text):
    text = text.replace('ä', 'ae')
    text = text.replace('ö', 'oe')
    text = text.replace('ü', 'ue')
    text = text.replace('ß', 'ss')
    return text


def replace_specific_substrings(text):
    text = text.replace('1er', 'einer')
    text = text.replace('2er', 'zweier')
    text = text.replace('3er', 'dreier')
    text = text.replace('4er', 'vierer')
    text = text.replace('5er', 'fünfer')
    text = text.replace('6er', 'sechser')
    text = text.replace('7/8', 'siebenachtel')
    return text


def remove_special_chars_and_numbers(text):
    new_text = ''
    for i in text:
        if i.isalnum() or i == ' ':
            new_text += i
    new_text = re.sub('[0-9]+','', new_text)

    _RE_COMBINE_WHITESPACE = re.compile(r"\s+")
    new_text = _RE_COMBINE_WHITESPACE.sub(" ", new_text).strip()

    return new_text


def stop_word_removal(text):
    german_stop_words = stopwords.words('german')
    token = text.split()
    return ' '.join([w for w in token if not w in german_stop_words])


def text_stemming(text):
    word_tokens = word_tokenize(text)
    words_tokens_lower = [word.lower() for word in word_tokens]

    words_filtered = [
        stemmer.stem(word) for word in words_tokens_lower
    ]
    return " ".join(words_filtered)


def clean_text(text):
    text = text.lower()

    text = replace_specific_letters(text)
    text = replace_specific_substrings(text)
    text = remove_special_chars_and_numbers(text)
    text = stop_word_removal(text)


    return text


def clean_columns(df, columns):
    for col in columns:
        df[col] = df[col].map(
            lambda x: clean_text(x) if isinstance(x, str) else x
        )
    return df
