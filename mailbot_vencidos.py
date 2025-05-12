import matplotlib.pyplot as plt # type: ignore
import numpy as np # type: ignore
import os # type: ignore
import pandas as pd # type: ignore
import smtplib # type: ignore
from datetime import datetime # type: ignore
from datetime import timedelta # type: ignore
from matplotlib.backends.backend_pdf import PdfPages # type: ignore
import pdfkit # type: ignore
from reportlab.lib.pagesizes import letter # type: ignore
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle # type: ignore
from reportlab.lib import colors # type: ignore
from my_lib import *
from mailbot import *

print(f"[ {pd.Timestamp.now()} ] Iniciando aplicação...")
print(f"[ {pd.Timestamp.now()} ] Buscando relatório no Thincake...")

def criar_vencidos():

    x = baixar_relatorio(1262).copy()

    print(f"[ {pd.Timestamp.now()} ] Relatório baixado, filtrando o mesmo...")

    for col in ['DATA_FATURAMENTO', 'DATA_NOTIFICACAO']:
        x[col] = pd.to_datetime(x[col], format='mixed', dayfirst=True)
        x[col] = x[col].dt.strftime('%d-%m-%Y')
        x[col] = pd.to_datetime(x[col], format='%d-%m-%Y', dayfirst=True)

    for col in ['CUSTO', 'CUSTO_TOTAL', 'QTD']:
        x[col] = x[col].astype(str).str.replace('[.]','', regex=True)
        x[col] = x[col].str.replace('[,]','.', regex=True).astype('float64')

    x['PRODUTO'] = x['PRODUTO'].str.strip()

    print(f"[ {pd.Timestamp.now()} ] Relatório criado")

    titulo = 'VENCIDOS'

    x = x[
        (x['DATA_FATURAMENTO'] >= segunda_passada) &
        (x['DATA_FATURAMENTO'] < hoje) &
        (x['AG'] == 531) &
        ((x['MOTIVO'].str.contains('VENC.', case=False, na=False)) == True)
        ]

    print(f"[ {pd.Timestamp.now()} ] Relatório filtrado")

    return x

def criar_vencidos_rede_tudo():

    x = criar_vencidos()

    x['SOMA_QTD'] = x.groupby(['COD_PROD'])['QTD'].transform('sum').astype('float64')
    x['SOMA_R$'] = x.groupby(['COD_PROD'])['CUSTO_TOTAL'].transform('sum').astype('float64')

    filtro = ['COD_PROD','PRODUTO','SOMA_QTD','SOMA_R$']

    x = x[filtro].drop_duplicates() \
        .sort_values(
            by=['SOMA_R$'],
            ascending=[False]
        )

    x.columns = ['CÓDIGO','PRODUTO','QTD','R$']

    print(f"[ {pd.Timestamp.now()} ] Relatório criado: VENCIDOS - REDE")

    return x

def criar_vencidos_rede(y):

    x = criar_vencidos()

    x = x[(x['NDEPTO'].str.contains(y, case=False, na=False))]

    x['SOMA_QTD'] = x.groupby(['COD_PROD'])['QTD'].transform('sum').astype('float64')
    x['SOMA_R$'] = x.groupby(['COD_PROD'])['CUSTO_TOTAL'].transform('sum').astype('float64')

    filtro = ['COD_PROD','PRODUTO','SOMA_QTD','SOMA_R$']

    x = x[filtro].drop_duplicates() \
        .sort_values(
            by=['SOMA_R$'],
            ascending=[False]
        )

    x.columns = ['CÓDIGO','PRODUTO','QTD','R$']

    print(f"[ {pd.Timestamp.now()} ] Relatório criado: VENCIDOS - REDE - {y}")

    return x

def criar_vencidos_lojas_tudo():

    x = criar_vencidos()

    x['SOMA_QTD'] = x.groupby(['FILIAL','COD_PROD'])['QTD'].transform('sum').astype('float64')
    x['SOMA_R$'] = x.groupby(['FILIAL','COD_PROD'])['CUSTO_TOTAL'].transform('sum').astype('float64')

    filtro = ['FILIAL','COD_PROD','PRODUTO','SOMA_QTD','SOMA_R$']

    x = x[filtro].drop_duplicates() \
        .sort_values(
            by=['SOMA_R$'],
            ascending=[False]
        )

    x = x[(x['SOMA_R$'] > 99.99)]
    x.columns = ['FILIAL','CÓDIGO','PRODUTO','QTD','R$']

    print(f"[ {pd.Timestamp.now()} ] Relatório criado: VENCIDOS - LOJAS")

    return x

def criar_vencidos_lojas(y):

    x = criar_vencidos()

    x = x[(x['NDEPTO'].str.contains(y, case=False, na=False))]

    x['SOMA_QTD'] = x.groupby(['FILIAL','COD_PROD'])['QTD'].transform('sum').astype('float64')
    x['SOMA_R$'] = x.groupby(['FILIAL','COD_PROD'])['CUSTO_TOTAL'].transform('sum').astype('float64')

    filtro = ['FILIAL','COD_PROD','PRODUTO','SOMA_QTD','SOMA_R$']

    x = x[filtro].drop_duplicates() \
        .sort_values(
            by=['SOMA_R$'],
            ascending=[False]
        )

    x = x[(x['SOMA_R$'] > 99.99)]
    x.columns = ['FILIAL','CÓDIGO','PRODUTO','QTD','R$']

    print(f"[ {pd.Timestamp.now()} ] Relatório criado: VENCIDOS - LOJAS - {y}")

    return x

def gerar_relatorios():

    vencidos_rede_tudo = criar_vencidos_rede_tudo()
    vencidos_rede_acougue_e_frios = criar_vencidos_rede('ACOUGUE|FRIOS')
    vencidos_rede_sem_pereciveis = criar_vencidos_rede('MERC')

    vencidos_lojas_tudo = criar_vencidos_lojas_tudo()
    vencidos_lojas_acougue_e_frios = criar_vencidos_lojas('ACOUGUE|FRIOS')
    vencidos_lojas_sem_pereciveis = criar_vencidos_lojas('MERC')

    relatorios = {
    'VENCIDOS - REDE': vencidos_rede_tudo,
    'VENCIDOS - ACOUGUE E FRIOS': vencidos_rede_acougue_e_frios,
    'VENCIDOS - MERCEARIA': vencidos_rede_sem_pereciveis,
    'VENCIDOS - LOJAS - TODOS': vencidos_lojas_tudo,
    'VENCIDOS - LOJAS - ACOUGUE E FRIOS': vencidos_lojas_acougue_e_frios,
    'VENCIDOS - LOJAS - MERCEARIA': vencidos_lojas_sem_pereciveis
    }

    return relatorios

def gerar_pdfs_vencidos():
    
    anexos = {}

    relatorios = gerar_relatorios()

    for titulo, relatorio in relatorios.items():
        print(f"[ {pd.Timestamp.now()} ] Gerando PDF em memória: {titulo}")

        copia = relatorio.copy()

        if copia.empty:
            print(f"[ {pd.Timestamp.now()} ] Nenhum dado para {titulo}. Pulando...")
            continue

        copia['QTD'] = pd.to_numeric(copia['QTD'], errors='coerce').round(4)
        copia['R$'] = pd.to_numeric(copia['R$'], errors='coerce').round(2)
        copia['R$'] = 'R$ ' + copia['R$'].apply(lambda x: f'{x:.2f}')

        pdf_buffer = io.BytesIO()
        data_periodo = f'{seg_pass} à {ont}'

        with PdfPages(pdf_buffer) as pdf:
            for i in range(0, len(copia), 55):
                b = copia.iloc[i:i+55]
                fig, ax = plt.subplots(figsize=(len(b.columns) * 2, 1))
                plt.suptitle(f'{titulo} - {data_periodo}', fontsize=16, fontweight='bold', y=(len(b) * 0.12))

                ax.axis('tight')
                ax.axis('off')

                table = ax.table(cellText=b.values, colLabels=b.columns, cellLoc='center', loc='center')
                table.auto_set_font_size(False)
                table.set_fontsize(10)
                table.auto_set_column_width(col=list(range(len(b.columns))))

                for i, cell in table._cells.items():
                    cell.set_edgecolor('lightgray')
                    if i[0] == 0:
                        cell.set_facecolor("green")
                        cell.set_text_props(weight="bold", color="white")
                        cell.set_edgecolor("white")

                for (row, col), cell in table.get_celld().items():
                    if col in [0, 1, 4]:
                        cell.set_text_props(weight="bold")
                    if row > 0:
                        cell.set_facecolor("0.95" if row % 2 == 0 else "white")
                    if (col == 3 or col == 4) and row > 0:
                        cell.set_text_props(weight="bold", color="white")
                        cell.set_facecolor("red")

                pdf.savefig(fig, bbox_inches="tight")
                plt.close()

        pdf_buffer.seek(0)
        nome_pdf = f"{titulo} - {seg_pass} A {ont}.pdf"
        anexos[nome_pdf] = pdf_buffer

        print(f"[ {pd.Timestamp.now()} ] PDF de {titulo} gerado.")

    return anexos

def enviar_vencidos():
    
    service = login()

    assunto = f"VENCIDOS - {seg_pass} À {ont}"

    corpo = f"""
    <div>

    Bom dia,
    <br>
    <br>
    Segue em anexo:
    <br>
    <br>
    <b>Sr. Glaucio</b>:&nbsp;<span class="il">Vencidos</span>&nbsp;- Geral
    <br>
    <b>Sr. Walter</b>:&nbsp;<span class="il">Vencidos</span>&nbsp;- Geral
    <br>
    <b>Sr. Marinho</b>:&nbsp;<span class="il">Vencidos</span>&nbsp;-&nbsp;<font color="#ff0000">Açougue e Frios&nbsp;</font><font color="#000000">e&nbsp;<span class="il">Vencidos</span>&nbsp;-&nbsp;</font><font color="#ff0000">Sem perecíveis.</font>
    <br>
    <br>
    Att.

    </div>
    """

    print(f"[ {pd.Timestamp.now()} ] Gerando PDFs para envio...")
    anexos = gerar_pdfs_vencidos()

    if anexos:
        destinatario = ",".join(['jocelene.paes@bistek.com.br','uzias.souza@bistek.com.br','central.cbm@bistek.com.br'])

        print(f"[ {pd.Timestamp.now()} ] Enviando e-mail para {destinatario}...")

        enviar_email(
            service,
            destinatario,
            assunto,
            corpo,
            html=True,
            multiplos_anexos=anexos
        )
    else:
        print(f"[ {pd.Timestamp.now()} ] Nenhum dado. E-mail não enviado.")

if __name__ == "__main__":
    enviar_vencidos()