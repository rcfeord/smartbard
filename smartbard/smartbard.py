import sys
from pathlib import Path

from image_model.image_keywords import image_to_keywords, select_keyword
from data_processing.bert_preproc import zorro, limerick_cleaner
from bert_model.bert_predict_masked_words import rhyme_word_pred
from data_processing.rhymes import make_rhymes, write_rhymes
from gpt2_model.gpt2 import gpt2_generate

KEYWORDS_N = 5 # number of keywords to extract from image
BEST_KEYWORDS_N = 1 # number of keywords to pick from extracted


def be_smart_be_bard(img_path: Path): # generate_limerick sounds too boring

    # set image path
    path = img_path # location of image on server, could also be passed as a blob, or pickle or tensor, ...

    # extract keywords from image
    image_keywords_df = image_to_keywords(path, KEYWORDS_N)
    keywords_list = select_keyword(image_keywords_df, BEST_KEYWORDS_N)

    # define starting sequence for GPT-2 generation
    start_sequence = f"<LS> <KS> {' '.join(keywords_list)} <KE>"

    #~~~~ Start of loop ~~~~~~
    while True:
        # generate limerick with GPT-2
        generated_limerick = gpt2_generate(start_sequence)

        # mask final words
        masked_limerick = zorro(generated_limerick)[0]

        # remove tokens
        masked_limerick_clean = limerick_cleaner(masked_limerick)

        # predict final words with BERT
        bert_words = rhyme_word_pred(masked_limerick_clean)

        # pick best rhymes
        rhymes = make_rhymes(bert_words)

        # exit loop if rhymes are found
        if rhymes:
            break
    #~~~~ End of loop ~~~~~~

    # produce final text
    final_limerick = write_rhymes(masked_limerick_clean, rhymes)


    return final_limerick


# if __name__ == '__main__':
#     be_smart_be_bard(sys.argv[1])
