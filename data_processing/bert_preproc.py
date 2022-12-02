import re

def zorro(limerick: str, line_numbers=[1,3,4]) -> str:
    """ masks last words of every verse of a limerick"""
    # set line numbers where to apply mask
    masked_ids = ''.join([str(n) for n in line_numbers])

    # let Zorro do his job
    masked_limerick = re.sub(fr'([a-zA-Z]+)([^a-zA-Z]*<L[{masked_ids}]>)', r'[MASK]\2', limerick)

    return masked_limerick
