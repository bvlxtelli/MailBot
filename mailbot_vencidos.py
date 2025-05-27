from my_lib import *
from mailbot import *
from modules import quebra_conhecida, pdf_creator

print(f"[ {pd.Timestamp.now()} ] Iniciando aplicação...")
print(f"[ {pd.Timestamp.now()} ] Buscando relatório no Thincake...")

def criar_vencidos(depto=None, loja=False):

    x = quebra_conhecida()

    x = x[
        (x['DATA_FATURAMENTO'] >= segunda_passada) &
        (x['DATA_FATURAMENTO'] < hoje) &
        ((x['MOTIVO'].str.contains('VENC.', case=False, na=False)) == True)
        ]

    if depto is not None:

        x = x[(x['NDEPTO'].str.contains(depto, case=False, na=False))]
    
    if loja is True:

        x['SOMA_QTD'] = x.groupby(['FILIAL','COD_PROD'])['QTD'].transform('sum').astype('float64')
        x['SOMA_R$'] = x.groupby(['FILIAL','COD_PROD'])['CUSTO_TOTAL'].transform('sum').astype('float64')
    
    else:

        x['SOMA_QTD'] = x.groupby(['COD_PROD'])['QTD'].transform('sum').astype('float64')
        x['SOMA_R$'] = x.groupby(['COD_PROD'])['CUSTO_TOTAL'].transform('sum').astype('float64')

    if loja is True:

        filtro = ['FILIAL','COD_PROD','PRODUTO','SOMA_QTD','SOMA_R$']
    
    else:

        filtro = ['COD_PROD','PRODUTO','SOMA_QTD','SOMA_R$']

    x = x[filtro].drop_duplicates() \
        .sort_values(
            by=['SOMA_R$'],
            ascending=[False]
        )

    if loja is True:

        x = x[(x['SOMA_R$'] > 99.99)]
        x.columns = ['FILIAL','CÓDIGO','PRODUTO','QTD','R$']
    
    else:

        x.columns = ['CÓDIGO','PRODUTO','QTD','R$']

    if loja is True and depto is not None:

        print(f"[ {pd.Timestamp.now()} ] Relatório criado: VENCIDOS - LOJAS - {depto}")
    
    elif loja is True and depto is None:

        print(f"[ {pd.Timestamp.now()} ] Relatório criado: VENCIDOS - LOJAS")
    
    elif loja is False and depto is not None:

        print(f"[ {pd.Timestamp.now()} ] Relatório criado: VENCIDOS - REDE - {depto}")
    
    elif loja is False and depto is None:

        print(f"[ {pd.Timestamp.now()} ] Relatório criado: VENCIDOS - REDE")

    return x

def gerar_relatorios():

    vencidos_rede_tudo = criar_vencidos(loja=False)
    vencidos_rede_acougue_e_frios = criar_vencidos(depto='ACOUGUE|FRIOS', loja=False)
    vencidos_rede_sem_pereciveis = criar_vencidos(depto='MERC', loja=False)

    vencidos_lojas_tudo = criar_vencidos(loja=True)
    vencidos_lojas_acougue_e_frios = criar_vencidos(depto='ACOUGUE|FRIOS', loja=True)
    vencidos_lojas_sem_pereciveis = criar_vencidos(depto='MERC', loja=True)

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

    Bom dia/tarde,
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
        
        destinatario = ",".join(['jocelene.paes@bistek.com.br','uzias.souza@bistek.com.br','central.cbm@bistek.com.br'])#['matheus.moura@bistek.com.br'])
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