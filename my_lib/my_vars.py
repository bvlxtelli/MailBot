from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from datetime import datetime
from datetime import timedelta
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from urllib import parse
import io
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import panel as pn
import re
import smtplib
import time
from io import StringIO
import requests
import urllib3
import pandas as pd
import chardet
from my_lib.paths import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Filiais ---

filiais = {'FILIAL': [2, 4, 5, 6, 7, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33]}
filiais = pd.DataFrame(filiais)
filiais['FILIAL'] = filiais['FILIAL'].astype(int)

filiais_com_digito = {'FILIAL': [27, 43, 51, 60, 78, 94, 108, 116, 124, 140, 167, 175, 183, 191, 205, 213, 221, 230, 248, 256, 264, 272, 299, 302, 310, 329, 337]}
filiais_com_digito = pd.DataFrame(filiais_com_digito)
filiais_com_digito['FILIAL'] = filiais_com_digito['FILIAL'].astype('int64')

lojas_com_digito = [27, 43, 51, 60, 78, 94, 108, 116, 124, 140, 167, 175, 183, 191, 205, 213, 221, 230, 248, 256, 264, 272, 299, 302, 310, 329, 337]
lojas_sem_digito = [2, 4, 5, 6, 7, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33]

# --- Dias & Datas ---

hoje = pd.Timestamp.now().strftime('%d-%m-%Y')
hoje = pd.to_datetime(hoje, format='%d-%m-%Y', dayfirst=True)
ontem = hoje - (timedelta(days=1))
anteontem = hoje - (timedelta(days=2))
sexta = hoje - (timedelta(days=3))

num_dia_da_semana = datetime.today().weekday()
semana = ('Segunda','Terça','Quarta','Quinta','Sexta','Sabado','Domingo')
dia_da_semana = semana[num_dia_da_semana]
sexta = hoje - (timedelta(days=3))
segunda_passada = hoje - (timedelta(days=7))

data_inicio_padrao = hoje - timedelta(days=15)

primeiro_dia_mes = hoje.replace(day=1)

dtmin = '01/01/1990'
dtmin = pd.to_datetime(dtmin, format='%d/%m/%Y', dayfirst=True)

hj = hoje.strftime('%d-%m-%Y')
ont = ontem.strftime('%d-%m')
anteont = anteontem.strftime('%d-%m')
seg_pass = segunda_passada.strftime('%d-%m')
sex = sexta.strftime('%d-%m')

# Data de corte pra planilhas diárias

xdias = 2
dias = timedelta(days=xdias)
dtct = (hoje - dias)

# Data de corte para seções atrasadas

max_ultimo_inventario = hoje - timedelta(days=500)

# --- Caminhos ---

py_csv_f = "C:\\Users\\Usuario\\Documents\\Python\\CSV\\"

# --- ---

relatorios = [
    40,
    274,    # Lançamentos
    1132,   # Venda (Para os bolos)
    1262,
    1334,
    1416,
    1501
    ]

planilhas_extras = [
    "agendas",
    "cronograma",
    "db suspeitos",
    "pereciveis",
    "secoes",
    "filiais"
]

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