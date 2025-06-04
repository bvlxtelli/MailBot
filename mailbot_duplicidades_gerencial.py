from my_lib import *
from mailbot import *
from modules import enviar_email_com_tabela

titulo = 'DIVERGÊNCIAS - GERENCIAL'

print(f"[ {pd.Timestamp.now()} ] Iniciando aplicação...")

def table_load():

    print(f"[ {pd.Timestamp.now()} ] Buscando relatório no Thincake...")

    x = baixar_relatorio(1124).copy()
    x = repair_things(x,float=['VALOR_GERENCIAL','VALOR_FISCAL','DIFERENCA'])

    print(f"[ {pd.Timestamp.now()} ] Relatório criado")

    return x

def enviar_duplicidades_gerenciais():
    
    service = login()

    a = table_load()

    if not a.empty:
        
        tabela_html = to_html_table(a)
        corpo_texto = """<p>Teste<p>"""

        assunto = f"{titulo} - {hj.strftime('%d-%m')}"
        corpo = f"""{corpo_texto}{tabela_html}"""

        destinatario = ','.join(['matheus.moura@bistek.com.br','daniel.santos@bistek.com.br','juliano.tavares@bistek.com.br'])
        print(f"[ {pd.Timestamp.now()} ] Enviando e-mail para {destinatario}...")

        enviar_email(
                service,
                destinatario,
                assunto,
                corpo,
                html=True
        )

    else:
         print(f"[ {pd.Timestamp.now()} ] Sem dados. E-mail não enviado. ✅")

if __name__ == "__main__":
    enviar_duplicidades_gerenciais()