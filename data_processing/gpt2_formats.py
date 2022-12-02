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


def tokenize_rhymes_ab(verse: str, line_number: int) -> str:
    """ add <RA> and <RB> tokens to the final word of a verse"""
    # example: "Should swallow a hand-grenade!"

    # split verse => ['Should', 'swallow', 'a', 'hand-grenade!']
    token_list = verse.split()
    # get last piece of the verse => 'hand-grenade!'
    last_index = max(loc for loc, val in enumerate(token_list) if re.search('[a-zA-Z]', val))
    last_token = token_list[last_index]
    # get code based on line number => <RA>
    a_lines = (0,1,4)
    b_lines = (2,3)
    if line_number in a_lines:
        code = '<RA>'
    elif line_number in b_lines:
        code = '<RB>'

    # add code before last token => ['Should', 'swallow', 'a', '<RA>', 'hand-grenade!']
    token_list_reversed = token_list[::-1]
    pos = token_list_reversed.index(last_token)
    token_list_reversed.insert(pos + 1, code)

    # return tokenized verse as a string => "Should swallow a <RA> hand-grenade!"
    return ' '.join(token_list_reversed[::-1])


def tokenize_rhymes_with_code(verse: str, encodings: dict) -> str:
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

def tokenize_rhymes_to_code(verse: str, encodings: dict) -> str:
    """ add <n> tokens to the final word of a verse"""
    #TODO: extract and then append punctuation to last word

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

    # substitute last token with its code => ['Should', 'swallow', 'a', '<8>']
    token_list[-1] = f'<{code}>'

    # return tokenized verse as a string => "Should swallow a <8>"
    return ' '.join(token_list)


def limerick_add_special_tkns(df: pd.DataFrame) -> pd.DataFrame:
    """
    add special tokens to the limerick:
    <LS> at the start of the limerick,
    <LA> at the start of each A line,
    <LB> at the start of each B line,
    <LE> at the end of each line,
    <n> before every final word on each line, where <n> represents the ending sounds.
    """
    # load encodings from json file to a dict
    encodings = load_encodings()
    # create 'limerick start' and 'limerick end' special tokens
    limerick_start = '<LS>'
    limerick_end = '<LE> '
    # create 'keyword start' and 'keyword end' special tokens
    keyword_start = '<KS>'
    keyword_end = '<KE>'
    # create a new empty column in df
    df['limerick_tk_added'] = ''
    # loop through each limerick
    for i in range(len(df)):
        # create keyword
        keyword = df['noun_keyword'].iloc[i]
        # create temp list containing limerick start token
        list_temp = [limerick_start, keyword_start, keyword, keyword_end]
        # split the limerick by line
        verses = df['limerick'].iloc[i].split('\n')

        # add special tokens to every verse
        for index, verse in enumerate(verses):
            start_tkn = '<LA> ' if index in (0, 1, 4) else '<LB> ' # token at the start of line
            # end_tkn = ' <LE>' # token at the end of line

            ### ALTERNATIVE_1: add rhyme tokens to the last words based on line num
            # verse = tokenize_rhymes_ab(verse, line_number=index)
            ### ALTERNATIVE_2: add rhyme tokens to the last words based on endings
            # verse = tokenize_rhymes_with_code(verse, encodings=encodings)
            ### ALTERNATIVE_3: substitute last words with tokens based on endings
            verse = tokenize_rhymes_to_code(verse, encodings=encodings)

            # append tokenized verse to temp list
            list_temp.append(start_tkn + verse)# + end_tkn)

        # add limerick end token to temp list
        list_temp.append(limerick_end)
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

def make_special_tokens_list() -> list:
    """ returns a special_tokens_list to be used as a value for the
    'additional_special_tokens' key in the special_tokens_dict"""
    # load rhyme codes
    encodings = load_encodings()

    # create list with special tokens
    special_tokens_list = ['<LA>', '<LB>', '<KS>', '<KE>']
    for val in encodings.values():
        special_tokens_list.append(f'<{val}>')

    return special_tokens_list
