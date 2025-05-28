from my_lib import *

def gerar_pdf(base=None, loja=None, titulo=None):

    rel = base
    
    if 'SEM VENDA' in titulo:
        
        rel.to_excel(f'C:\\Users\\Usuario\\Downloads\\ESPELHO - ITENS SEM VENDA - {hj}.xlsx', index=False)
    
        colunas = ['NOME_DPTO', 'NOME_SECAO', 'PRODUTO', 'DESCRICAO', 'LOJA']
        copia_do_relatorio = rel.copy()
        a = copia_do_relatorio[copia_do_relatorio['LOJA'] == loja][colunas].reset_index(drop=True)
        skus = a['LOJA'].value_counts().get(loja, 0)

    if 'PENDENTES' in titulo:

        colunas = ['DPTO', 'SECAO', 'CODIGO', 'DESCRICAO', 'FILIAL']
        copia_do_relatorio = rel.copy()
        a = copia_do_relatorio[
            (copia_do_relatorio['FILIAL'] == loja) &
            (copia_do_relatorio['SITUACAO'] == 'NAO INV')][colunas].drop_duplicates().reset_index(drop=True)
        skus = len(a)

    #if 'QUEBRA' in titulo or 'VENCIDOS' in titulo:

    #    'a'

    if a.empty:
        print(f"[ {pd.Timestamp.now()} ] Nenhum dado para a loja {loja}.")
        return None

    contador_de_linhas = 0
    pdf_buffer = io.BytesIO()

    if 'PENDENTES' in titulo or 'SEM VENDA' in titulo: 

        with PdfPages(pdf_buffer) as pdf:
        
            while contador_de_linhas < skus:

                if 'SEM VENDA' in titulo or 'PENDENTES' in titulo:
                    b = a.iloc[contador_de_linhas:(contador_de_linhas + 45)]

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

    if 'QUEBRA' in titulo or 'VENCIDOS' in titulo:
    
        copia = base.copy()

        if copia.empty:
            print(f"[ {pd.Timestamp.now()} ] Nenhum dado. Cancelando...")
            return None

        copia['QTD'] = pd.to_numeric(copia['QTD'], errors='coerce').round(4)
        copia['R$'] = pd.to_numeric(copia['R$'], errors='coerce').round(2)
        copia['R$'] = 'R$ ' + copia['R$'].apply(lambda x: f'{x:.2f}')

        if 'MAIORES' in titulo:
            data_periodo = f'{anteont} à {ont}' if dia_da_semana != 'Segunda' else f'{sex} à {ont}'
        
        elif 'VENCIDOS' in titulo:
            data_periodo = f'{seg_pass} à {ont}'

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
        print(f"[ {pd.Timestamp.now()} ] PDF gerado em memória.")

        return pdf_buffer