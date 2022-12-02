import nltk
import pandas as pd
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def extract_noun_keyword(text: str) -> str:
    """
    extracts nouns from text and return the first noun
    """
    tokenized = nltk.word_tokenize(text)
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if(pos[:2] == 'NN')]
    try:                        #            #
        return nouns[0]         # TEMPORARY  #
    except:                     # WORKAROUND #
        return ''               #            #

def df_add_noun_keyword(df: pd.DataFrame, column_name='limerick') -> pd.DataFrame:
    """
    adds a noun keyword for each limerick to a new column of the pd.DataFrame
    """
    df['noun_keyword'] = df['limerick'].apply(extract_noun_keyword)
    return df
