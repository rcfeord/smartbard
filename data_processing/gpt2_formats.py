import pandas as pd

def limerick_add_special_tkns(df: pd.DataFrame) -> pd.DataFrame:
    """
    add a special token at the start of the limerick and at the end of each line
    """
    # create a new empty column in df
    df['limerick_tk_added'] = ''
    # loop through each limerick
    for i in range(len(df)):
        # create the 'limerick start' special token
        list_temp = ['<LS>']
        # split the limerick by line
        verses = df['limerick'].iloc[i].split('\n')
        # add a special token at the end of each line
        for verse in verses:
            list_temp.append(verse + ' <LE>')
        # join the strings in the list and add to new df column
        list_temp = ' '.join(list_temp)
        df['limerick_tk_added'].iloc[i] = list_temp
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
