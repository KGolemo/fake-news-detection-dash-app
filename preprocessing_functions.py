#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
from polyglot.detect import Detector
from polyglot.downloader import downloader
import re
import morfeusz2
from typing import List

downloader.download('LANG:pl')


def drop_title_and_url(df: pd.DataFrame) -> pd.DataFrame:
    """Drops 'Title' and 'Url' columns.

    Args:
        df (pd.Dataframe): News dataset.

    Returns:
        pd.Dataframe: News dataset without 'Title' and 'Url' columns.
    """
    return df.drop(columns=['Title', 'Url'])


def drop_empty(df: pd.DataFrame) -> pd.DataFrame:
    """Drops empty rows.

    Args:
        df (pd.Dataframe): News dataset.

    Returns:
        df (pd.Dataframe): News dataset without empty rows.
    """
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def drop_non_polish(df: pd.DataFrame) -> pd.DataFrame:
    """Detects and drops non-polish articles.

    Args:
        df (pd.Dataframe): News dataset containing non-polish articles.

    Returns:
        df (pd.Dataframe): News dataset containing only polish articles.
    """
    for index, row in df.iterrows():
        text = row['Text']
        detector = Detector(text, quiet=True)
        if not (detector.language.name == 'Polish' and
                detector.language.confidence >= 70):
            df.drop([index], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def drop_unidentified(df: pd.DataFrame) -> pd.DataFrame:
    """Drops news with 'unidentified' verdict.

    Args:
        df (pd.Dataframe): News dataset containing 'unidentified' news.

    Returns:
        pd.Dataframe: News dataset containing only fake or real news.
    """
    return df[df['Verdict'] != 'unidentified']


def drop_twitter(df: pd.DataFrame) -> pd.DataFrame:
    """Drops news from twitter containing some website elements.

    Args:
        df (pd.Dataframe): News dataset containing news with some website elements.

    Returns:
        pd.Dataframe: News dataset without noisy twitter news.
    """
    return df[df['Text'].str.contains('Nowy na Twitterze')==False]


def change_verdict_dtype(df: pd.DataFrame) -> pd.DataFrame:
    """Changes data type of 'Verdict' column to boolean.

    Args:
        df (pd.Dataframe): News dataset.

    Returns:
        df (pd.Dataframe): News dataset with boolean 'Verdict' column.
    """
    df['Verdict'].replace('false', 0, inplace=True)
    df['Verdict'].replace('true', 1, inplace=True),
    df['Verdict'] = df['Verdict'].astype(bool)
    return df


def drop_short(df: pd.DataFrame) -> pd.DataFrame:
    """Drops articles shorter than 30 characters.

    Args:
        df (pd.Dataframe): News dataset.

    Returns:
        pd.Dataframe: News dataset with articles not shorter than 30 chars.
    """
    return df[df['Text'].apply(len) >= 30]


def delete_escape_chars(text: str) -> str:
    """Replaces escape characters with single whitespace.

    Args:
        text (str): Input article.

    Returns:
        ret_text (str): Processed article.
    """
    ret_text = text.replace('\\n', ' ').replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
    return ret_text


def strip_non_polish(text: str) -> str:
    """Replaces non-polish characters with single whitespace.

    Args:
        text (str): Input article.

    Returns:
        ret_text (str): Processed article.
    """
    reg = re.compile('[^a-zA-ZĄąĆćĘęŁłŃńÓóŚśŹźŻż]')
    ret_text = reg.sub(' ', text)
    return ret_text


def replace_whitespace(text: str) -> str:
    """Replaces multiple whitespaces with single whitespace.

    Args:
        text (str): Input article.

    Returns:
        ret_text (str): Processed article.
    """
    reg = re.compile('\s+')
    ret_text = reg.sub(' ', text)
    return ret_text


def lowercase_all(text: str) -> str:
    """Converts case of article.

    Args:
        text (str): Input article.

    Returns:
        ret_text (str): Processed article.
    """
    ret_text = str.lower(text)
    return ret_text


def tokenize(text: str) -> List[str]:
    """Performs tokenization by splitting articles into words.

    Args:
        text (str): Input article.

    Returns:
        ret_text (str): Processed article.
    """
    ret_text = str.split(text)
    return ret_text


def delete_stop_words(text: str) -> List[str]:
    """Removes stopwords.

    Args:
        text (str): Input article containing stopwords.

    Returns:
        ret_text (str): Processed article.
    """
    stop_words_txt = open('stopwords.txt')
    stop_words = stop_words_txt.read().split('\n')
    stop_words_txt.close()
    ret_text = [word for word in text if word not in stop_words]
    return ret_text


def lemmatize(df: pd.DataFrame) -> pd.DataFrame:
    """Performs lemmatization of articles in dataset.

    Args:
        df (pd.Dataframe): News dataset.

    Returns:
        df (pd.Dataframe): Lemmatized news dataset.
    """
    morf = morfeusz2.Morfeusz()
    for index, row in df.iterrows():
        text = row['Text']
        lemm_words = []
        for word in text:
            _, _, interpretation = morf.analyse(word)[0]
            lem_word = interpretation[1]
            lem_word_stripped = lem_word.split(':', 1)[0].lower()
            lemm_words.append(lem_word_stripped)
        df.loc[index, 'Text'] = ' '.join(lemm_words)
    return df
