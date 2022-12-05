import pandas as pd
import cmudict

# file_path = '../raw_data/limerick_dataset_oedilf_v3.json'

def data_import_df(file_path: str) -> pd.DataFrame:
    """
    imports data from json file and returns a pandas DataFrame of true limericks
    """
    # import json as DataFrame
    df = pd.read_json(file_path)
    # keep only true limericks
    df = df[df.is_limerick == True]
    return df

def extract_lines(df: pd.DataFrame) -> list:
    """
    imports DataFrame of true limericks
    returns a list of single verse lines
    """
    # separate limericks into lines and store in list
    lines = []
    for i in range(len(df)):
        verses = df['limerick'].iloc[i].split('\n')
        for verse in verses:
            lines.append(verse)
    return lines

def extract_ab_lines(df: pd.DataFrame) -> list:
    """
    extracts A and B lines from a DataFrame containing limericks,
    returns a tuple with two lists: (a_lines, b_lines)
    """
    a_lines = []
    b_lines = []

    for i in range(len(df)):
        x = df.iloc[i,1].splitlines()
        a_lines += x[:2] + [x[4]]
        b_lines += (x[2:4])

    return a_lines, b_lines

def decompose_word(string: str) -> list:
    """
    takes a word (str) as input and returns a list with its phonetic decomposition
    """
    words = cmudict.entries()
    words_dict = {}
    for word in words:
        words_dict[word[0]] = word[1]

    return words_dict.get(string, 'UNKNOWN')


def word_ending(word: str) -> list:
    """
    takes a word (str) as input and returns a list only of
    endings (sounds after last stress)
    """
    ending = []
    sounds = decompose_word(word)
    index = 0
    for i in range(len(sounds)):
        if "1" in sounds[i] or "2" in sounds[i]:
            index = i

    ending = sounds[index:]

    return ending

# DEPRECATED
def dict_of_sounds(list_of_words: list) -> dict:
    """
    takes a list of words (str) as input and returns a dict
    with words as keys and endings as values
    """
    sounds = {}
    for word in list_of_words:
        sounds[word] = word_ending(word)

    return sounds

def dict_of_endings() -> dict:
    """
    generates a dict of ending sounds from the cmudict list
    """
    endings = {}
    for el in cmudict.entries():
        word = el[0]
        sounds = el[1]
        sounds_reversed = sounds[::-1]

        index = len(sounds)
        for sound in sounds_reversed:
            if "1" in sound or "2" in sound:
                index = sounds_reversed.index(sound)
                break

        ending = sounds_reversed[:index + 1][::-1]
        endings[word] = ending

    return endings

def encode_unique_patterns() -> dict:
    """
    takes the cmudict endings as input and returns a dict
    with words as keys and encoded sound patterns (endings) as values
    """

    # get the endings of the cmudict
    endings = dict_of_endings()

    # take only the words from endings

    words = list(endings.keys())

    # take only sound patterns from  endings
    patterns = list(endings.values())

    # sort the sound patterns alphabetically
    sorted_patterns = sorted(patterns)

    # get only the unique sound patterns
    unique_patterns = []
    for pattern in sorted_patterns:
        if pattern not in unique_patterns:
            unique_patterns.append(pattern)

    # encode the unique sound pattern
    encoded_patterns = {}
    for key, value in zip(range(1, len(unique_patterns)+1), unique_patterns):
        encoded_patterns[key] = value

    # map keys from cmudict endings and keys from encoded patterns (as values)
    for key, value in endings.items():
        for key2, value2 in encoded_patterns.items():
            if value == value2:
                endings[key] = key2

    return endings
