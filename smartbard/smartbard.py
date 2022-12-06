#########################
## THIS IS A DRAFT !!! ##
#########################
import sys

from smartbard.image_model.image_keywords import image_to_keywords, select_keyword
from smartbard.data_processing.bert_preproc import zorro, limerick_cleaner
from smartbard.bert_model.bert_predict_masked_words import rhyme_word_pred
from smartbard.data_processing.rhymes import make_rhymes

KEYWORDS_N = 5 # number of keywords to extract from image
BEST_KEYWORDS_N = 1 # number of keywords to pick from extracted
#TODO: do we need both of these? One should suffice


def be_smart_be_bard(img: type_to_be_defined): # generate_limerick sounds too boring

    # set image path
    path = pass # location of image on server, could also be passed as a blob, or pickle or tensor, ...

    # extract keywords from image
    image_keywords_df = image_to_keywords(path, KEYWORDS_N)
    keywords_list = select_keyword(image_keywords_df, BEST_KEYWORDS_N)

    # define starting sequence for GPT-2 generation
    start_sequence = f"<LS> <KS> {' '.join(keywords_list)} <KE> "

    # generate limerick with GPT-2
    generated_limerick = generated_text(sequence) #TODO: gpt2, or a module that calls it, needs to be imported

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
