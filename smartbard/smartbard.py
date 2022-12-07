#########################
## THIS IS A DRAFT !!! ##
#########################
import sys

from smartbard.image_model.image_keywords import image_to_keywords, select_keyword
from smartbard.data_processing.bert_preproc import zorro, limerick_cleaner
from smartbard.bert_model.bert_predict_masked_words import rhyme_word_pred
from smartbard.data_processing.rhymes import make_rhymes
from smartbard.gpt2_model.gpt2 import gpt2_generate

KEYWORDS_N = 5 # number of keywords to extract from image
BEST_KEYWORDS_N = 1 # number of keywords to pick from extracted
#TODO: do we need both of these? One should suffice


def be_smart_be_bard(img_path: str): # generate_limerick sounds too boring

    # set image path
    path = img_path # location of image on server, could also be passed as a blob, or pickle or tensor, ...

    # extract keywords from image
    image_keywords_df = image_to_keywords(path, KEYWORDS_N)
    keywords_list = select_keyword(image_keywords_df, BEST_KEYWORDS_N)

    # define starting sequence for GPT-2 generation
    start_sequence = f"<LS> <KS> {' '.join(keywords_list)} <KE>"

    # generate limerick with GPT-2
    generated_limerick = gpt2_generate(start_sequence)

    #### TEMP ##### TODO: delete this
    # import os
    # import pandas as pd
    # import numpy as np
    # data_folder = '../raw_data/'
    # data_file = 'limerick_dataset_oedilf_v3.json'
    # file = os.path.join(data_folder, data_file)
    # df_raw = pd.read_json(file)
    # df_raw[df_raw['is_limerick'] == True]
    # num = np.random.randint(0,100)
    # limerick = df_raw['limerick'].iloc[num]
    ##############

    # mask final words
    masked_limerick = zorro(generated_limerick)[0]

    # remove tokens
    masked_limerick_clean = limerick_cleaner(masked_limerick)

    # predict final words with BERT
    bert_words = rhyme_word_pred(masked_limerick_clean)

    # pick best rhymes and produce final text
    final_limerick = make_rhymes(masked_limerick_clean, bert_words)


    return final_limerick


if __name__ == '__main__':
    be_smart_be_bard(sys.argv[1]) #TODO: define a way to pass image to python module

    #TODO: return API response with final text
