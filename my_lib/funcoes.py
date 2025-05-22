from .my_vars import *
from .paths import *

def carregar_relatorio(x):

    try:
        with open(REL_PATHS[x], 'rb') as f:
            rawdata = f.read(10000)
            result = chardet.detect(rawdata)
            encoding = result['encoding']

            if encoding is None or encoding.lower() == 'ascii':
                encoding = 'utf-8'
        return pd.read_csv(REL_PATHS[x], delimiter=';', encoding=encoding)
    
    except UnicodeDecodeError:
        return pd.read_csv(REL_PATHS[x], delimiter=';', encoding='latin1')