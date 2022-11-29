import pandas as pd

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
