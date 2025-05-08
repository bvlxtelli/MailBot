from my_lib import *
from mailbot import *

#agd = pd.read_csv('C:\\Users\\Usuario\\Downloads\\relatorio_274-28-04-2025.csv', delimiter=';')

def agenda_656(y):

    x = y

    x = x[x['AGENDA'] == 656]

    x['DT_AGENDA'] = pd.to_datetime(x['DT_AGENDA'], format='mixed', dayfirst=True)
    x['DT_AGENDA'] = x['DT_AGENDA'].dt.strftime('%d-%m-%Y')
    x['DT_AGENDA'] = pd.to_datetime(x['DT_AGENDA'], format='%d-%m-%Y', dayfirst=True)

    for col in ['VLR_TOTAL','VLR_NOTA','VL_CUSTO_NF','VL_CUSTO_TABELA','QUANTIDADE']:

        x[col] = x[col].str.replace('[.]','', regex=True)
        x[col] = x[col].str.replace('[,]','.', regex=True).astype('float64')

    x['PRODUTO'] = x['PRODUTO'].str.replace('[-]','', regex=True).astype('int64')

    if dia_da_semana == 'Segunda':
    
        x = x[(x['DT_AGENDA'] == ontem) | (x['DT_AGENDA'] == anteontem) | (x['DT_AGENDA'] == sexta)]
        
    else:

        x = x[x['DT_AGENDA'] == ontem]

    x = filiais.merge(x, on=['FILIAL'], how='left')
    x = x.groupby('FILIAL')['QUANTIDADE'].sum()

    x = pd.DataFrame(x).reset_index()

    return x

def enviar_sacolas():

    agd = agenda_656(baixar_relatorio(274))

    service = login()

    for loja, emails in ccp_sem_digito.items():

        if dia_da_semana == 'Segunda':
    
            titulo = f"BAIXAS DE SACOLAS - LOJA {loja} -  {sexta.strftime('%d')}, {anteontem.strftime('%d')} E {ontem.strftime('%d/%m')}"
            tal_dia = f'{sexta.strftime('%d')}, {anteontem.strftime('%d')} e {ontem.strftime('%d/%m/%Y')}'
        
        else:

            titulo = f"BAIXAS DE SACOLAS - LOJA {loja} - {ontem.strftime('%d/%m')}"
            tal_dia = ontem.strftime('%d/%m/%Y')

        assunto = f'{titulo}'

        agd_x = agd.loc[agd['FILIAL'] == loja]

        if not agd_x.empty:

            quantidade = agd_x['QUANTIDADE'].values[0]

            if quantidade == 0:

                corpo = f"""
                <p>Boa dia/tarde,</p>

                <p>Após análise, verificamos que a loja citada (Loja <strong>{loja}</strong>) <strong>não realizou as baixas de sacolas</strong> na agenda <strong>656</strong>, no(s) dia(s) <strong>{tal_dia}</strong>.</p>

                <p><strong>Favor verificar</strong>, o <strong>recomendado</strong> e realizar as <strong>baixas todos os dias</strong> e de pelo menos <strong>1 fardo (1.000 unidades)</strong>.</p>

                <p>Em caso de dúvidas, sinalizar <a href="mailto:central.cbm@bistek.com.br" target="_blank">@central.cbm</a>.</p>
                """
    
            elif 0 < quantidade < 500:

                corpo = f"""
                <p>Boa tarde,</p>

                <p>Após análise, verificamos que a loja citada (Loja <strong>{loja}</strong>) baixou apenas <strong><font size="4">{agd_x['QUANTIDADE'].values[0]} unidade(s)</font></strong> de sacolas na agenda <strong>656</strong>, no(s) dia(s) <strong>{tal_dia}</strong>.</p>

                <p><strong>Favor verificar</strong>, o <strong>recomendado</strong> e realizar as <strong>baixas todos os dias</strong> e de pelo menos <strong>1 fardo (1.000 unidades)</strong>.</p>

                <p>Em caso de dúvidas, sinalizar <a href="mailto:central.cbm@bistek.com.br" target="_blank">@central.cbm</a>.</p>
                """
            
            else:

                print(f"[ {pd.Timestamp.now()} ] Loja {loja} sem dados. E-mail não enviado.")
                continue
        
            destinatario = ','.join(emails)
            print(f"[ {pd.Timestamp.now()} ] Enviando e-mail para {destinatario}...")

            enviar_email(
                service,
                destinatario,
                assunto,
                corpo,
                html=True
            )

if __name__ == "__main__":
    enviar_sacolas()