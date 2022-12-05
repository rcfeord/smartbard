import re

def zorro(limerick: str, *line_numbers: int) -> tuple:
    """
    masks last words of every verse of a limerick,
    returns masked limerick and a list of masked words

    arguments:
        limerick: str
        line_numers (optionals): ints, line numbers to mask
                                 defaults to 1, 3, 4
    returns a tuple of len 2:
        output[0]: masked_limerick,
        output[1]: { 'masked':  [(line_num, masked_word),  ... ],
                    'unmasked': [(line_num, unmasked_word), ...] }
    """
    # assert correct format of line_numbers: comma separated positive integers
    for i in range(len(line_numbers)):
        assert type(line_numbers[i]) == int and line_numbers[i] >= 0,\
            'line_numbers should be positive ints'

    # set line numbers where to and where not to apply mask
    line_numbers = sorted(list(set(line_numbers))) if line_numbers else [1,3,4] # default values
    lines = [0,1,2,3,4]
    nomask_line_numbers = list(set(lines)-set(line_numbers))

    # set masked and unmasked ids based on line_numbers
    masked_ids = ''.join([str(n) for n in line_numbers])
    unmasked_ids = ''.join([str(n) for n in nomask_line_numbers]) + r'\0'

    # define regex patterns
    compile_pattern = lambda ids: fr'([a-zA-Z]+)([^a-zA-Z]*<L[{ids}]>)'
    pattern = compile_pattern(masked_ids)
    anti_pattern = compile_pattern(unmasked_ids)

    # search and store words to be masked
    search = re.findall(pattern, limerick)
    masked_words = [(n, group[0]) for n, group in zip(line_numbers, search)]

    # search and store not masked final words
    anti_search = re.findall(anti_pattern, limerick)
    unmasked_words = [(n, group[0]) for n, group in zip(nomask_line_numbers, anti_search)]

    # let Zorro do his job
    masked_limerick = re.sub(pattern, r'[MASK]\2', limerick)

    return masked_limerick, {'masked': masked_words, 'unmasked': unmasked_words}


def limerick_cleaner(limerick:str) -> str:
    """ removes tokens and keywords from a limerick """
    # remove keywords
    step1 = re.sub(r'(<KS>.*<KE>\s)', r'', limerick)
    # substitute '<L#>' with '\n'
    step2 = re.sub(r'(<[A-Z][0123]>\s)', r'\n', step1)
    # clean up the remaining tokens
    step3 = re.sub(r'(<[A-Z][\w]>\s)', r'', step2)
    # strip white spaces
    limerick_clean = step3.strip()

    return limerick_clean
