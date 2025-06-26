from my_lib import *
from mailbot import *

print(f"[ {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} ] Iniciando aplicação...")
print(f"[ {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} ] Buscando relatório no Thincake...")

def maiores_quebras(df):

    #for col in ['COD_PROD', 'COD_DEPTO', 'COD_SECAO', 'COD_FORNECEDOR', 'FILIAL', 'AG']:

    #    df[col] = df[col].astype('int64')

    for col in ['DATA_FATURAMENTO', 'DATA_NOTIFICACAO']:

        df[col] = pd.to_datetime(df[col], format='mixed', dayfirst=True)
        df[col] = df[col].dt.strftime('%d-%m-%Y')
        df[col] = pd.to_datetime(df[col], format='%d-%m-%Y', dayfirst=True)

    for col in ['CUSTO', 'CUSTO_TOTAL', 'QTD']:

        df[col] = df[col].str.replace('[.]', '', regex=True)
        df[col] = df[col].str.replace('[,]', '.', regex=True).astype('float64')

    df['PRODUTO'] = df['PRODUTO'].str.strip()
    df['NDEPTO'] = df['NDEPTO'].str.strip()

    print(f"[ {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} ] Relatório criado")

    if dia_da_semana != 'Segunda':
        df = df[(df['DATA_FATURAMENTO'] >= anteontem) & (df['DATA_FATURAMENTO'] < hoje)]
    else:
        df = df[(df['DATA_FATURAMENTO'] < hoje) & (df['DATA_FATURAMENTO'] >= sexta)]
    
    df = df[(df['NDEPTO'] == 'FLV - HORTIFRUTI') & (df['AG'] == 531)]
    df['SOMA_QTD'] = df.groupby(['FILIAL', 'COD_PROD'])['QTD'].transform('sum')
    df['SOMA_R$'] = df.groupby(['FILIAL', 'COD_PROD'])['CUSTO_TOTAL'].transform('sum')
    df = df[['FILIAL', 'COD_PROD', 'PRODUTO', 'SOMA_QTD', 'SOMA_R$']].drop_duplicates()
    df = df.sort_values(by='SOMA_R$', ascending=False)
    df = df[df['SOMA_R$'] > 199.99]
    df.columns = ['FILIAL', 'CÓDIGO', 'PRODUTO', 'QTD', 'R$']

    return df

def gerar_pdf_mqc():

    mqc = maiores_quebras(baixar_relatorio(1262))
    
    copia = mqc.copy()

    if copia.empty:
        print(f"[ {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} ] Nenhum dado. Cancelando...")
        return None

    copia['QTD'] = pd.to_numeric(copia['QTD'], errors='coerce').round(4)
    copia['R$'] = pd.to_numeric(copia['R$'], errors='coerce').round(2)
    copia['R$'] = 'R$ ' + copia['R$'].apply(lambda x: f'{x:.2f}')

    pdf_buffer = io.BytesIO()
    titulo = 'MAIORES QUEBRAS CONHECIDAS - FLV'
    data_periodo = f'{anteont} à {ont}' if dia_da_semana != 'Segunda' else f'{sex} à {ont}'

    with PdfPages(pdf_buffer) as pdf:

        for i in range(0, len(copia), 50):
            b = copia.iloc[i:i+50]
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
    print(f"[ {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} ] PDF gerado em memória.")

    return pdf_buffer

def enviar_maiores_quebras():

    service = login()
    titulo = 'MAIORES QUEBRAS CONHECIDAS - FLV'
    periodo = f'{anteont} À {ont}' if dia_da_semana != 'Segunda' else f'{sex} À {ont}'

    assunto = f"{titulo} - {periodo}"
    corpo = f"""<p>Bom dia/tarde,</p>
    
    <p>Segue relatório citado em anexo (Entregar para o Sr. Marinho).</p>
    
    <p>Att.</p>"""

    print(f"[ {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} ] Gerando PDF para loja...")
    pdf_buffer = gerar_pdf_mqc()

    if pdf_buffer:

        nome_pdf = f"{assunto.replace("À", "A")}.pdf"
        destinatario = ",".join(['jocelene.paes@bistek.com.br','maurici@bistek.com.br','uzias.souza@bistek.com.br','central.cbm@bistek.com.br'])

        print(f"[ {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} ] Enviando e-mail para {destinatario}...")
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

        print(f"[ {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} ] Sem dados. E-mail não enviado.")

if __name__ == "__main__":
    enviar_maiores_quebras()