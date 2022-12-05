import pandas as pd
from data_processing.gpt2_formats import load_encodings

def bert_to_df_list(bert_words: tuple) -> list:
    """ converts a collection of words returned by BERT to a list of DataFrames

    bert_words has the following format
    (
        [('word1', prob1), ('word2', prob2), ...],
        [('word1', prob1), ('word2', prob2), ...],
        ...
    )

    Output is a list of DataFrames: [df1, df2, ...]
    """
    # load rhyme encodings
    encodings = load_encodings()

    def words_list_to_df():
        # convert the list into a DataFrame
        column_names = ['word', 'probability']
        words_df = pd.DataFrame(bert_words, columns=column_names)
        # add a column with the rhyme encoding
        code_col = words_df.apply(lambda row: encodings.get(row['word']), axis=1)
        words_df.insert(0, 'code', code_col)

        return words_df

    df_list = []
    for words_list in bert_words:
        words_df = words_list_to_df(words_list)
        df_list.append(words_df)

    return df_list


def proba_score(df: pd.DataFrame) -> pd.Series:
    """
    returns a Series containing the scores calculated on
    the given probabilities
    """
    # set columns containing probabilities
    proba_cols = [col for col in df.columns if 'probability' in col]
    # collect probability values in a generator
    probabilities = (df[col] for col in proba_cols)

    # define scoring function
    alpha = 0.1
    score = lambda x: (1 + alpha) * x / (x + alpha)

    # compute total score
    total_score = 1
    for p in probabilities:
        total_score *= score(p)

    return total_score

def best_rhymes(df_list: list) -> list:
    """ picks best combination of rhyming words

        df_list is a list of data frames

        ouput is a list of words
    """

    # merge data frames on the condition that words have the same rhyming code
    length = len(df_list)
    if length == 3:
        combos_df = pd.merge(df_list[0], df_list[1], on =['code']).merge(df_list[2], on =['code'])
    elif length == 2:
        combos_df = pd.merge(df_list[0], df_list[1], on =['code'])
    else:
        raise TypeError('Argument has wrong format')

    # add column with a score for each word combination
    combos_df['score'] = proba_score(combos_df)
    # select combination with highest score
    best_combo_df = combos_df.nlargest(1,['score'])
    # create a list with the words from the best combination
    word_cols = [col for col in best_combo_df.columns if 'word' in col]
    words = [best_combo_df[col].values[0] for col in word_cols]

    return words
