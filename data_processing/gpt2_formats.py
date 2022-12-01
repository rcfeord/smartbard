import pandas as pd
import re
import json
import os


def load_encodings() -> dict:
    """ loads rhymes encoding from a json file and returns a dictionary"""
    json_file_name = "cmudict_encoded.json"
    # set path of json file
    encodings_path = os.path.join(os.path.dirname(__file__), json_file_name)

    # read file content and store into a dictionary
    with open(encodings_path, 'r') as json_file:
        encodings_dict = json.load(json_file)

    return encodings_dict


def limerick_add_special_tkns(df: pd.DataFrame) -> pd.DataFrame:
    """
    add special tokens to the limerick:
    <LS> at the start of the limerick,
    <LA> at the start of each A line,
    <LB> at the start of each B line,
    <LE> at the end of each line,
    <n> before every final word on each line, where <n> represents the ending sounds.
    """
    def tokenize_rhymes(verse: str) -> str:
        """ add <n> tokens to the final word of a verse"""
        # example: "Should swallow a hand-grenade!"

        # split verse => ['Should', 'swallow', 'a', 'hand-grenade!']
        token_list = verse.split()
        # get last piece of the verse => 'hand-grenade!'
        last_index = max(loc for loc, val in enumerate(token_list) if re.search('[a-zA-Z]', val))
        last_token = token_list[last_index]
        # extract last real word (containing only alphabetic characters) => 'grenade'
        last_word = [token for token in re.split('[^a-zA-Z]', last_token) if token.isalpha()][-1]
        # get code number for its ending sounds => 8
        code = encodings.get(last_word, -1)

        # add code before last token => ['Should', 'swallow', 'a', '<8>', 'hand-grenade!']
        token_list_reversed = token_list[::-1]
        pos = token_list_reversed.index(last_token)
        token_list_reversed.insert(pos + 1, f'<{code}>')

        # return tokenized verse as a string => "Should swallow a <8> hand-grenade!"
        return ' '.join(token_list_reversed[::-1])

    # load encodings from json file to a dict
    encodings = load_encodings()
    # create a new empty column in df
    df['limerick_tk_added'] = ''
    # loop through each limerick
    for i in range(len(df)):
        # create the 'limerick start' special token
        list_temp = ['<LS>']
        # split the limerick by line
        verses = df['limerick'].iloc[i].split('\n')

        # add a special tokens
        for index, verse in enumerate(verses):
            start_tkn = '<LA> ' if index in (0, 1, 4) else '<LB> ' # token at the start of line
            end_tkn = ' <LE>' # token at the end of line

            # add rhyme tokens to the last words
            verse = tokenize_rhymes(verse)
            # append tokenized verse to list_temp
            list_temp.append(start_tkn + verse + end_tkn)

        # join the strings in the list and add to new df column
        limerick_with_tkns = ' '.join(list_temp)
        df['limerick_tk_added'].iloc[i] = limerick_with_tkns

    return df


def limerick_reverse(df: pd.DataFrame, column_name='limerick_tk_added') -> pd.DataFrame:
    """
    reverse the order of the words in a limerick
    """
    # create a new empty column in df
    df['limerick_tk_reversed'] = ''
    # loop through each limerick
    for i in range(len(df)):
        list_temp = df[column_name].iloc[i]
        # split the words in the limerick
        words = list_temp.split(' ')
        # then reverse the split string list and join using space
        reverse_sentence = ' '.join(reversed(words))
        # add to new column in df
        df['limerick_tk_reversed'].iloc[i] = reverse_sentence
    return df


def all_words_encoded() -> str:
    """ returns a string with all the words from the cmudict prefixed by their respective tokens """
    encodings = load_encodings()
    # instantiate final string
    final_string = ''
    for word, code in encodings.items():
        # add token and word to final string
        final_string += f'<{code}> {word} '

    return final_string
