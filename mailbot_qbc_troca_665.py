from my_lib import *
from mailbot import *

def agendas(x,y):

    a = x.copy()

    a = a[a['AGENDA'] == 665]

    a['DT_AGENDA'] = pd.to_datetime(a['DT_AGENDA'], format='mixed', dayfirst=True)
    a['DT_AGENDA'] = a['DT_AGENDA'].dt.strftime('%d-%m-%Y')
    a['DT_AGENDA'] = pd.to_datetime(a['DT_AGENDA'], format='%d-%m-%Y', dayfirst=True)

    for col in ['VLR_TOTAL','VLR_NOTA','VL_CUSTO_NF','VL_CUSTO_TABELA','QUANTIDADE']:

        a[col] = a[col].astype(str).str.replace('[.]','', regex=True)
        a[col] = a[col].str.replace('[,]','.', regex=True).astype('float64')

    a['PRODUTO'] = a['PRODUTO'].str.replace('[-]','', regex=True).astype('int64')

    b = y.copy()

    b_filtro = ['RMS','CODIGO_FORNECEDOR','NOME_FORNECEDOR']

    b['CODIGO_FORNECEDOR'] = b['CODIGO_FORNECEDOR'].astype(str)
    b = b[b_filtro]
    b = b.rename(columns={'RMS': 'PRODUTO'})

    a = a.merge(b, on=['PRODUTO'], how='left')
    a = a.sort_values(by=['DT_AGENDA','VLR_TOTAL','DESCRICAO','NR_NOTA','NOME_FORNECEDOR'],ascending=False)
    a_filtro = ['CODIGO_FORNECEDOR','NOME_FORNECEDOR','PRODUTO','DESCRICAO','QUANTIDADE','VLR_TOTAL','AGENDA','FILIAL','NR_NOTA','DT_AGENDA']
    a = a[a_filtro]

    if dia_da_semana == 'Segunda':

        a = a[(a['DT_AGENDA'] == ontem) & (a['CODIGO_FORNECEDOR'].isin(['107123','173630','272850','84445','450200','460028','476536','481947']))]
    
    else:

        a = a[((a['DT_AGENDA'] == ontem) | (a['DT_AGENDA'] == anteontem) | (a['DT_AGENDA'] == sexta) ) & (a['CODIGO_FORNECEDOR'].isin(['107123','173630','272850','84445','450200','460028','476536','481947']))]

    return a

def enviar_qbc_troca_665():
    
    service = login()

    a = agendas(baixar_relatorio(274),baixar_relatorio(40))

    for loja, emails in ccp_sem_digito.items():
        
        print(f"[ {pd.Timestamp.now()} ] Gerando dados para loja {loja}...")

        dados_loja = a[a['FILIAL'] == loja]

        if not dados_loja.empty:

            tabela_html = dados_loja.to_html(index=False, justify='center', border=0, classes='tabela-pereciveis')
            tabela_html = tabela_html.replace(
            "<table>",
            """<table style="border-collapse:collapse;width:100%;font-family:Arial, sans-serif;font-size:14px">""")
            tabela_html = tabela_html.replace(
            "<th>",
            """<th style="text-align:center;padding:8px;border-bottom:2px solid #4682b4;background-color:#e6f2ff;color:#003366">""")
            tabela_html = tabela_html.replace(
            "<td>",
            """<td style="padding:6px;text-align:center;border-bottom:1px solid #ddd">""")

            titulo = f"TROCA LANÇADA NA QUEBRA - AGENDA 665 - LOJA {loja} - {ontem.strftime('%d/%m')}"
            assunto = f'{titulo}'
            
            corpo = f"""
            <p>Boa dia/tarde,</p>

            <p>Segue abaixo os lançamentos indevidos realizados na <strong>agenda 665</strong> no <strong>dia {ontem.strftime('%d/%m')}</strong> na Loja <strong>{loja}</strong>.</p>

            {tabela_html}

            <p>Favor verificar, pois são produtos <strong>troca que foram lançadas(os) na quebra de forma indevida</strong>.</p>

            <p>Em caso de dúvidas, sinalizar <a href="mailto:central.cbm@bistek.com.br" target="_blank">@central.cbm</a>.</p>
            """

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
    
    enviar_qbc_troca_665()