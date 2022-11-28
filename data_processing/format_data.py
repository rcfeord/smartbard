import pandas as pd

# file_path = '../raw_data/limerick_dataset_oedilf_v3.json'

def extract_lines(file_path):
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
