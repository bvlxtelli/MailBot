import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import numpy as np
import io
from datetime import datetime, timedelta
from my_lib import *
from mailbot import *

titulo = 'SUSPEITOS PENDENTES'

dtmin = pd.to_datetime('01/01/1990', format='%d/%m/%Y', dayfirst=True)
dias = timedelta(days=2)
dtct = hoje - dias

def carregar_dados(a,b):

    bdsus = carregar_relatorio("db suspeitos")
    bdinv = a
    bdcg = b
    
    bdcg.columns = ['NUM_INV', 'DESCRICAO_INV', 'DATA_CG', 'FILIAL', 'DESC_FILIAL', 'CODIGO', 'DESCRICAO', 'NUM_SECAO', 'DESC_SECAO']

    bdsus = bdsus[['DATA', 'SOLICITADO', 'SUSPEITO', 'CODIGO', 'FILIAL']]
    bdinv = bdinv[['DPTO', 'SECAO', 'CODIGO', 'DESCRICAO', 'FILIAL', 'DATA_ULT_INV']]
    bdcg = bdcg[['DATA_CG', 'CODIGO', 'FILIAL']]

    bdg = bdsus.merge(bdinv, on=['CODIGO', 'FILIAL'])
    bdg = bdg.merge(bdcg, on=['CODIGO', 'FILIAL'], how='left')

    for col in ['DATA', 'DATA_ULT_INV', 'DATA_CG']:

        bdg[col] = pd.to_datetime(bdg[col], format='mixed', dayfirst=True)
        bdg[col] = bdg[col].dt.strftime('%d-%m-%Y')
        bdg[col] = pd.to_datetime(bdg[col], format='%d-%m-%Y', dayfirst=True)

    bdg['SITUACAO'] = np.where(
        (bdg['DATA_ULT_INV'] >= bdg['DATA']) & (~bdg['DPTO'].isna()), 'INV',
        np.where((bdg['DATA_CG'] > dtmin) & (~bdg['DPTO'].isna()), 'INV', 'NAO INV')
    )

    bdg = bdg.sort_values(by=['DPTO', 'SECAO', 'DESCRICAO'], ascending=True)
    return bdg


def gerar_pdf_lj_suspeitos(loja, dados_filtrados):

    colunas = ['DPTO', 'SECAO', 'CODIGO', 'DESCRICAO', 'FILIAL']
    a = dados_filtrados[(dados_filtrados['FILIAL'] == loja) & (dados_filtrados['SITUACAO'] == 'NAO INV')][colunas].drop_duplicates()
    
    if a.empty:
        print(f"[ {pd.Timestamp.now()} ] Nenhum dado para a loja {loja}.")
        return None

    skus = a['FILIAL'].value_counts().get(loja, 0)
    contador_de_linhas = 0
    pdf_buffer = io.BytesIO()

    with PdfPages(pdf_buffer) as pdf:
        while contador_de_linhas < skus:
            b = a.iloc[contador_de_linhas:contador_de_linhas + 45]
            fig, ax = plt.subplots(figsize=(len(b.columns) * 1.5, 1))
            ax.axis('tight')
            ax.axis('off')

            table = ax.table(cellText=b.values, colLabels=b.columns, cellLoc='center', loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.auto_set_column_width(col=list(range(len(b.columns))))

            for i, cell in table._cells.items():
                cell.set_edgecolor('lightgray')
                if i[0] == 0:
                    cell.set_facecolor("black")
                    cell.set_text_props(weight="bold", color="white")
                    cell.set_edgecolor("white")

            for (row, col), cell in table.get_celld().items():
                if col == 2 or col == 4:
                    cell.set_text_props(weight="bold")

            for (row, col), cell in table.get_celld().items():
                if row > 0:
                    cell.set_facecolor("0.95" if row % 2 == 0 else "white")

            pdf.savefig(fig, bbox_inches="tight")
            plt.close()
            contador_de_linhas += 45

    pdf_buffer.seek(0)
    print(f"[ {pd.Timestamp.now()} ] PDF da Loja {loja} gerado em memória.")

    return pdf_buffer

def enviar_suspeitos_pendentes():
    
    service = login()
    destinatario_var = inventario_com_digito
    lojas = list(destinatario_var.keys())

    dados = carregar_dados(baixar_relatorio(1334), baixar_relatorio(1416))

    for loja in lojas:
        
        emails = destinatario_var[loja]
        titulo_email = f"{titulo} - LOJA {loja}"
        assunto = f"(URGENTE) {titulo_email}"
        corpo = f"Bom dia/tarde,\n\nSegue em anexo relatório de suspeitos que ainda <strong>não foram realizados</strong>."

        print(f"[ {pd.Timestamp.now()} ] Gerando PDF para loja {loja}...")
        pdf_buffer = gerar_pdf_lj_suspeitos(loja, dados)

        if pdf_buffer:

            nome_pdf = f"{titulo_email} - {datetime.now().strftime('%d-%m')}.pdf"
            destinatario = ','.join(emails)

            print(f"[ {pd.Timestamp.now()} ] Enviando e-mail para {destinatario}...")

            enviar_email(
                service,
                destinatario,
                assunto,
                corpo,
                html=True,
                caminho_anexo=None,
                anexo_buffer=pdf_buffer,
                nome_anexo=nome_pdf
            )

        else:

            print(f"[ {pd.Timestamp.now()} ] Nenhum dado para a loja {loja}. E-mail não enviado.")

if __name__ == "__main__":
    enviar_suspeitos_pendentes()