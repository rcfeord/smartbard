import re

def zorro(limerick: str, line_numbers=[1,3,4]) -> str:
    """ masks last words of every verse of a limerick"""
    # set line numbers where to apply mask
    masked_ids = ''.join([str(n) for n in line_numbers])

    # let Zorro do his job
    masked_limerick = re.sub(fr'([a-zA-Z]+)([^a-zA-Z]*<L[{masked_ids}]>)', r'[MASK]\2', limerick)

    return masked_limerick


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
