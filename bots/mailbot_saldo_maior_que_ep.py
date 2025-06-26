from __base__ import *

titulo = 'SALDO MAIOR QUE ESTOQUE PADRÃO'

print(f"[ {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} ] Iniciando aplicação...")

def table_load():

    print(f"[ {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} ] Buscando relatório no Thincake...")

    x = baixar_relatorio(1132).copy()

    print(f"[ {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} ] Relatório criado")

    x = x[x['QTD_SALDO_LOJA'] > x['EP']]
    x = x[['LOJA','CODIGO','DESCRICAO','QTD_SALDO_LOJA','EP']]

    return x

def enviar_saldo_maior_que_ep():
    
    service = login()

    try:

        a = table_load()

        if not a.empty:
        
            tabela_html = to_html_table(a)
            corpo_texto = """<p>Segue relação de itens que estão com o saldo maior que o estoque padrão.<p>"""

            assunto = f"{titulo} - {hoje.strftime('%d-%m')}"
            corpo = f"""{corpo_texto}{tabela_html}"""

            destinatario = ','.join(central_cbm + 'lucas.sedrez@bistek.com.br')
            print(f"[ {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} ] Enviando e-mail para {destinatario}...")

            enviar_email(
                service,
                destinatario,
                assunto,
                corpo,
                html=True
            )

        else:
            print(f"[ {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} ] Sem dados. E-mail não enviado. ✅")

    except:

        print(f"[ {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} ] Dataframe vazio, pulando função...")


if __name__ == "__main__":
    enviar_saldo_maior_que_ep()