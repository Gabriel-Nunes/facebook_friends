import sys
def show_exception_and_exit(exc_type, exc_value, tb):
    '''
    Avoid console screen shut down after errors.
    '''
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("\nPressione qualquer tecla para sair...")
    sys.exit(-1)

from unicodedata import normalize
from re import sub


def normaliza(txt):
    """
    Replace non ASCII characters for its equivalent ones.

    Replace double spaces at the begining or the end of a string.

        >>> normaliza('[ACENTUAÇÃO] ç: áàãâä! éèêë? íìîï, óòõôö; úùûü.')
        '[ACENTUACAO] c: aaaaa! eeee? iiii, ooooo; uuuu.'
    """
    result = normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
    result.strip()
    result = sub('\s{2,}', ' ', result)
    return result
