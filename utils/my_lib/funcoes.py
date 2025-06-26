from .my_vars import *
from .paths import *

titulo = "Funções"

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
    
# --- Repair ---
    
def string_repair(x, y):
    for z in y:
        x[z] = x[z].astype('string').str.strip()
    return x

def float_repair(x,y):
    
    for z in y:

        x[z] = x[z].str.replace('[.]','', regex=True)
        x[z] = x[z].str.replace('[,]','.', regex=True).astype('float64')

    return x

def strip_repair(x,y):

    for z in y:

        x[z] = x[z].astype(str).str.strip()

    return x

def date_repair(x, y):
    for z in y:
        x[z] = pd.to_datetime(x[z], format='mixed', dayfirst=True)
        x[z] = x[z].dt.strftime('%d-%m-%Y')
        x[z] = pd.to_datetime(x[z], format='%d-%m-%Y', dayfirst=True)
    return x

def int_repair(x, y):
    for z in y:
        x[z] = x[z].astype('int64')
    return x

def repair_things(df=None, string=None, strip=None, float=None, date=None, int=None):

    if string is not None:
        string_repair(df, string)
    
    if strip is not None:
        strip_repair(df, strip)
    
    if float is not None:
        float_repair(df, float)
    
    if date is not None:
        date_repair(df, date)
    
    if int is not None:
        int_repair(df, int)

    return df

def to_html_table(dados):

    tabela_html = dados.to_html(index=False, justify='center', border=0, classes='tabela-pereciveis')
    tabela_html = tabela_html.replace(
        "<table>",
        """<table style="border-collapse:collapse;width:100%;font-family:Arial, sans-serif;font-size:14px">""")
    tabela_html = tabela_html.replace(
        "<th>",
        """<th style="text-align:center;padding:8px;border-bottom:2px solid #adadad;background-color:#676767;color:#ffffff">""")
    tabela_html = tabela_html.replace(
        "<td>",
        """<td style="padding:6px;text-align:center;border-bottom:1px solid #ddd">""")
    
    return tabela_html

print(f"[ {pd.Timestamp.now()} ] Módulo {titulo} carregado")