from my_lib import *
from mailbot import *

def criar_pereciveis():

    bdcrono = repair_things(df=carregar_relatorio("cronograma"), string=['SECAO'], date=['DATA'])
    bdsecoes = repair_things(df=carregar_relatorio("secoes"), string=['CODIGO_SECAO', 'DESCRICAO_SECAO', 'CODIGO_DPTO', 'DESCRICAO_DPTO','Qtd. Produtos'])
    bdsecoes.columns = ['SECAO','DESCRICAO_SECAO','DPTO','DESCRICAO_DPTO','Qtd. Produtos']
    bdperec = repair_things(carregar_relatorio("pereciveis"), string=['PERECIVEIS', 'SECAO'])
    bdsecoes = bdsecoes.merge(bdperec, on='SECAO', how='left').fillna('-')
    inventarios = repair_things(df=carregar_relatorio("relatorio_1334"), string=['CODIGO', 'DESCRICAO', 'DPTO', 'SECAO','DIAS_ULT_INV'], date=['DATA_ULT_INV'], int=['FILIAL'], float=['SALDO'])
    congelados = repair_things(df=carregar_relatorio("relatorio_1416"), string=['NUM_INV', 'DESCRICAO_INV', 'DESC_FILIAL', 'RMS','DESCRICAO', 'SECAO', 'DESC_SECAO'], date=['DATA'], int=['FILIAL'])
    congelados.columns = ['NUM_INV','DESCRICAO_INV','DATA_CG','FILIAL','DESC_FILIAL','CODIGO','DESCRICAO','SECAO','DESC_SECAO']
    congelados_filtro = ['DATA_CG','FILIAL','CODIGO']
    congelados = congelados[congelados_filtro]

    crono = bdcrono.merge(bdsecoes, on='SECAO', how='left').fillna('-')

    df_base_repeated = pd.concat([filiais_com_digito] * len(crono), ignore_index=True)
    df_ref_repeated = crono.loc[crono.index.repeat(len(filiais_com_digito))].reset_index(drop=True)
    df_final = pd.concat([df_ref_repeated, df_base_repeated], axis=1)
    df_final = df_final.sort_values(by='FILIAL',ascending=True)
    df_final = df_final.dropna()
    df_final['SECAO'] = df_final['SECAO'].astype(str) + " - " + df_final['DESCRICAO_SECAO']
    df_final['DPTO'] = df_final['DPTO'].astype(str) + " - " + df_final['DESCRICAO_DPTO']
    df_final_filtro = ['DATA','DPTO','SECAO','FILIAL','PERECIVEIS']
    df_final = df_final[df_final_filtro]

    cronograma = df_final.merge(inventarios, on=['DPTO','SECAO','FILIAL'], how='left').dropna()
    cronograma = cronograma.merge(congelados, on=['CODIGO','FILIAL'], how='left')
    cronograma['DATA'] = cronograma['DATA'].fillna('01/01/1990')
    cronograma['DATA_CG'] = cronograma['DATA_CG'].fillna('01/01/1990')
    cronograma = repair_things(df=cronograma, date=['DATA','DATA_ULT_INV','DATA_CG'], string=['DPTO','SECAO','PERECIVEIS','CODIGO','DESCRICAO','SALDO','DIAS_ULT_INV'], int=['FILIAL'])
    cronograma.insert(
        loc = 11,
        column = 'SITUACAO',
        value = np.where(
        (cronograma['DATA_ULT_INV'] >= primeiro_dia_mes),
        'INV',
        (np.where(
        (cronograma['DATA_CG'] > dtmin),
        'INV',
        'NAO INV')
        )
        )
        )

    a = cronograma[cronograma['PERECIVEIS'] == 'PERECIVEIS']

    return a

def pendentes(x,y):

    pln_um = (
                        x.groupby(['DATA','DPTO','SECAO','FILIAL'])
                        .size()
                        .reset_index(name='SIZE')
                        .fillna(0)
    )

    pln_dois = (
                        x[x['SITUACAO'] == 'INV'].groupby(['DATA','DPTO','SECAO','FILIAL'])
                        .size()
                        .reset_index(name='INV')
                        .fillna(0)
    )

    pln_pend = pln_um.merge(pln_dois, how='left').fillna(0)

    pln_pend.insert(
        loc = 6,
        column = 'SITUACAO',
        value = np.where((pln_pend['INV'] >= (0.75*(pln_pend['SIZE']))),'INV','NAO INV')
        )
    
    pln_pend = pln_pend[(pln_pend['SITUACAO'] == 'NAO INV') & (pln_pend['DATA'] < hoje) & (pln_pend['FILIAL'] == y)]

    pln_pend_filtro = ['FILIAL','DATA','DPTO','SECAO']
    pln_pend = pln_pend[pln_pend_filtro]

    pln_pend = pln_pend.sort_values(by=['FILIAL','DATA','DPTO','SECAO'], ascending=[True, True, True, True])
    pln_pend = pln_pend.drop_duplicates()

    return pln_pend

def enviar_pereciveis():
    
    service = login()

    pereciveis = criar_pereciveis()

    for loja, emails in inventario_com_digito.items():
        
        print(f"[ {pd.Timestamp.now()} ] Gerando dados para loja {loja}...")

        dados_loja = pendentes(pereciveis, loja)

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

            titulo = f"PERECÍVEIS PENDENTES - LOJA {loja}"
            assunto = f'{titulo}'

            corpo = f"""
            <p>Bom dia/tarde,</p>

            <p>Segue abaixo os perecíveis que estão pendentes na loja <strong>{loja}</strong>.</p>

            {tabela_html}

            <p><strong>É dever do setor</strong> entregar todos os perecíveis até o final do mês.</p>
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
    enviar_pereciveis()