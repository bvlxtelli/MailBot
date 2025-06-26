from __base__ import *

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

    bdg = bdg[(bdg['DATA'] < ontem)]

    bdg = bdg.sort_values(by=['DPTO', 'SECAO', 'DESCRICAO'], ascending=True)

    return bdg

def enviar_suspeitos_pendentes():
    
    service = login()

    for loja, emails in inventario_com_digito.items():
        
        titulo = f"SUSPEITO - PENDENTES - LOJA {loja}"
        assunto = f"(URGENTE) {titulo}"
        corpo = f"Bom dia/tarde,\n\nSegue em anexo relatório de suspeitos que ainda <strong>não foram realizados</strong>."

        print(f"Gerando PDF para loja {loja}...")

        dados = carregar_dados(baixar_relatorio(1334), baixar_relatorio(1416))
        pdf_buffer = gerar_pdf(base=dados, loja=loja, titulo=titulo)

        if pdf_buffer:

            nome_pdf = f"{titulo} - {datetime.now().strftime('%d-%m')}.pdf"
            destinatario = ','.join(emails)

            print(f"Enviando e-mail para {destinatario}...")

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
            print(f"Loja {loja} sem dados. E-mail não enviado.")

if __name__ == "__main__":
    enviar_suspeitos_pendentes()