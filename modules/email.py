from my_lib import *
from mailbot import *

def enviar_email_com_tabela(base,grupo,titulo_texto,corpo_texto):
    
    service = login()

    a = base

    for loja, emails in grupo.items():
        
        print(f"[ {pd.Timestamp.now()} ] Gerando dados para loja {loja}...")

        dados_loja = a[(a['FILIAL'].astype(int)) == loja]

        if not dados_loja.empty:

            tabela_html = dados_loja.to_html(index=False, justify='center', border=0, classes='tabela-pereciveis')
            tabela_html = tabela_html.replace(
            "<table>",
            """<table style="border-collapse:collapse;width:100%;font-family:Arial, sans-serif;font-size:14px">""")
            tabela_html = tabela_html.replace(
            "<th>",
            """<th style="text-align:center;padding:8px;border-bottom:2px solid #adadad;background-color:#676767;color:#ffffff">""")
            tabela_html = tabela_html.replace(
            "<td>",
            """<td style="padding:6px;text-align:center;border-bottom:1px solid #ddd">""")

            if dia_da_semana != 'Segunda':

                titulo = f"{titulo_texto} - {ontem.strftime('%d/%m')} - LOJA {loja}"

            else:

                titulo = f"{titulo_texto} - {sexta.strftime('%d')}, {ontem.strftime('%d')} E {anteontem.strftime('%d/%m')} - LOJA {loja}"
            
            assunto = titulo
            corpo = f"""{corpo_texto}{tabela_html}"""

            destinatario = ','.join(emails)
            print(f"[ {pd.Timestamp.now()} ] Enviando e-mail para {destinatario}...")

            enviar_email(
                service,
                destinatario,
                assunto,
                corpo,
                html=True
            )

        else:
            print(f"[ {pd.Timestamp.now()} ] Loja {loja} sem dados. E-mail não enviado.")

if __name__ == "__main__":
    
    enviar_email_com_tabela()
