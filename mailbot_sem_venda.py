import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import io
import os
import pandas as pd # type: ignore
from datetime import datetime # type: ignore
from datetime import timedelta # type: ignore
import matplotlib.pyplot as plt # type: ignore
from matplotlib.backends.backend_pdf import PdfPages # type: ignore
import smtplib # type: ignore
import os # type: ignore
from my_lib import *
from mailbot import *

x_dias = 45 # Dias
dias = timedelta(days=x_dias)
dsv = (hoje - dias)

def sem_venda(x):

    y = x

    for col in ['ULTIMAVENDA', 'DATA_INVENTARIO', 'DTULTENTRADA']:

        y[col] = pd.to_datetime(y[col], format='mixed', dayfirst=True)
        y[col] = y[col].dt.strftime('%d-%m-%Y')
        y[col] = pd.to_datetime(y[col], format='%d-%m-%Y', dayfirst=True)

    y = y.sort_values(
    
        by=['NOME_DPTO','NOME_SECAO','PRODUTO','DESCRICAO','LOJA'],
        ascending=[True, True, True, True, True]
    )

    y = y[
        (y['DATA_INVENTARIO'] < dsv ) &
        (y['ULTIMAVENDA'] < dsv ) &
        (y['DTULTENTRADA'] < dsv)
    ]

    return y

def gerar_pdf_lj_sem_venda(loja):

    rel = sem_venda(baixar_relatorio(1217))

    rel.to_excel(f'C:\\Users\\Usuario\\Downloads\\ESPELHO - ITENS SEM VENDA - {hj}.xlsx', index=False)
    
    colunas = ['NOME_DPTO', 'NOME_SECAO', 'PRODUTO', 'DESCRICAO', 'LOJA']
    copia_do_relatorio = rel.copy()
    copia_do_relatorio = copia_do_relatorio[copia_do_relatorio['LOJA'] == loja][colunas]

    if copia_do_relatorio.empty:
        print(f"Nenhum dado para a loja {loja}.")
        return None

    skus = rel['LOJA'].value_counts().get(loja, 0)
    contador_de_linhas = 0
    pdf_buffer = io.BytesIO()

    with PdfPages(pdf_buffer) as pdf:
        while contador_de_linhas < skus:
            b = copia_do_relatorio.iloc[contador_de_linhas:(contador_de_linhas + 45)]

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
    print(f"PDF da Loja {loja} gerado em memória.")
    
    return pdf_buffer

def enviar_sem_venda():

  service = login()
  
  for loja, emails in inventario_com_digito.items():
    
    titulo = f"SUSPEITO - SEM VENDA - LOJA {loja}"

    assunto = f'(URGENTE) {titulo}'
    corpo = f"Boa dia/tarde,\n\nSegue em anexo suspeito de produtos que estão há mais de 30 dias sem venda na loja.\n\nEsse suspeito passa a ser semanal, ou seja, caso não seja feito irá acumular para a semana seguinte."

    print(f"Gerando PDF para loja {loja}...")
    
    pdf_buffer = gerar_pdf_lj_sem_venda(loja)

    if pdf_buffer:
        
      nome_pdf = f"{titulo} - {datetime.now().strftime('%d-%m')}.pdf"
      destinatario = ','.join(emails)

      print(f"Enviando e-mail para {destinatario}...") 
        
      enviar_email(
        service,
        destinatario,
        assunto,
        corpo,
        caminho_anexo=None,
        anexo_buffer=pdf_buffer,
        nome_anexo=nome_pdf
      )

    else:
      
      print(f"Loja {loja} sem dados. E-mail não enviado.")

if __name__ == "__main__":
    enviar_sem_venda()