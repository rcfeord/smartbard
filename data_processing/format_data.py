import pandas as pd
import cmudict

# file_path = '../raw_data/limerick_dataset_oedilf_v3.json'

def extract_lines(file_path: str) -> list:
    """
    imports data from json file and returns a list of single verse lines from true limericks
    """

    # import json as DataFrame
    df = pd.read_json(file_path)
    # keep only true limericks
    true_limerick_df = df[df.is_limerick == True]

    # separate limericks into lines and store in list
    lines = []
    for i in range(len(true_limerick_df)):
        verses = true_limerick_df['limerick'].iloc[i].split('\n')
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


def word_ending(word: str) -> dict:
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

def dict_of_sounds(list_of_words: list) -> dict:
    """
    takes a list of words (str) as input and returns a dict 
    with words as keys and endings as values 
    """
    sounds = {}
    for word in list_of_words:
        sounds[word] = word_ending(word)
    
    return sounds
