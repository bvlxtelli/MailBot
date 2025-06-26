from my_lib import *
from mailbot import *

def agendas(x,y):

    a = x.copy()

    a = a[a['AGENDA'] == y]

    a['DT_AGENDA'] = pd.to_datetime(a['DT_AGENDA'], format='mixed', dayfirst=True)
    a['DT_AGENDA'] = a['DT_AGENDA'].dt.strftime('%d-%m-%Y')
    a['DT_AGENDA'] = pd.to_datetime(a['DT_AGENDA'], format='%d-%m-%Y', dayfirst=True)

    for col in ['VLR_TOTAL','VLR_NOTA','VL_CUSTO_NF','VL_CUSTO_TABELA','QUANTIDADE']:

        a[col] = a[col].str.replace('[.]','', regex=True)
        a[col] = a[col].str.replace('[,]','.', regex=True).astype('float64')

    a['PRODUTO'] = a['PRODUTO'].str.replace('[-]','', regex=True).astype('int64')

    b = a.copy()

    a = a[(a['DT_AGENDA'] >= (hoje - (timedelta(days=7))))]
    a = filiais.merge(a, on=['FILIAL'], how='left')
    a = a.groupby('FILIAL')['VLR_TOTAL'].sum()
    a = pd.DataFrame(a).reset_index()
    a['VLR_TOTAL'] = a['VLR_TOTAL'] / 7
    a = a.rename(columns={'VLR_TOTAL': 'VLR_SEMANA'})

    b = filiais.merge(b, on=['FILIAL'], how='left')
    b = b.groupby('FILIAL')['VLR_TOTAL'].sum()
    b = pd.DataFrame(b).reset_index()
    b['VLR_TOTAL'] = b['VLR_TOTAL'] / 90
    b = b.rename(columns={'VLR_TOTAL': 'VLR_MEDIA'})
    
    a = a.merge(b, on=['FILIAL'], how='left')

    return a

def enviar_agendas_por_valor():

    agds ={'DOAÇÃO PREVENÇÃO':160,
           'ESPAÇO CAFÉ':599}

    service = login()

    x = baixar_relatorio(274)

    for nome_agenda, agenda in agds.items():

        agd = agendas(x, agenda)

        for loja, emails in ccp_sem_digito.items():
            
            titulo = f"BAIXAS SEMANAIS - AGENDA {agenda} - {nome_agenda} - LOJA {loja}"
            #tal_dia = f'{sexta.strftime('%d')}, {anteontem.strftime('%d')} e {ontem.strftime('%d/%m/%Y')}'

            assunto = f'{titulo}'

            agd_x = agd.loc[agd['FILIAL'] == loja]

            if not agd_x.empty:

                qtd_semana = agd_x['VLR_SEMANA'].values[0]
                qtd_media = agd_x['VLR_MEDIA'].values[0]

                if qtd_semana < (qtd_media * 0.85) and qtd_media != 0:

                    corpo = f"""
                    Bom dia/tarde,
                    <p>Após análise, verificamos que a loja citada (Loja <strong>{loja}</strong>) está com as baixas na agenda <strong><font size="4">{agenda} - {nome_agenda}</font></strong> <strong><font size="4" color="blue">ABAIXO</font> da média da loja</strong>.</p>
                    <p>A <strong>média diária</strong> é de <strong><font size="4">R$ {round(qtd_media)}</font></strong>, e foram baixadas(os), <strong>nos últimos 7 dias</strong>, <strong>em média</strong> <strong><font size="4" color="red">R$ {round(qtd_semana)}</font></strong> por dia. Totalizando <strong><font size="4">R$ {round((qtd_semana) * 7)}</font></strong>.</p>
                    <p><strong>Favor verificar de forma urgente</strong>, o <strong>recomendado</strong> é realizar as <strong>baixas de forma constante</strong> para evitar quebras e/ou disperdícios.</p>
                    <p>Em caso de dúvidas, sinalizar <a href="mailto:central.cbm@bistek.com.br" target="_blank">@central.cbm</a>.</p>
                    """
                
                elif qtd_semana > (qtd_media * 1.85) and qtd_media != 0:

                    corpo = f"""
                    Boa dia/tarde,
                    <p>Após análise, verificamos que a loja citada (Loja <strong>{loja}</strong>) está com as baixas na agenda <strong><font size="4">{agenda} - {nome_agenda}</font></strong> <strong><font size="4" color="red">ACIMA</font> da média da loja</strong>.</p>
                    <p>A <strong>média diária</strong> é de <strong><font size="4">R$ {round(qtd_media)}</font></strong>, e foram baixadas(os), <strong>nos últimos 7 dias</strong>, <strong>em média</strong> <strong><font size="4" color="red">R$ {round(qtd_semana)}</font></strong> por dia. Totalizando <strong><font size="4">R$ {round((qtd_semana) * 7)}</font></strong>.</p>
                    <p><strong>Favor verificar de forma urgente</strong> se não foi realizado nenhuma <strong>baixa indevida</strong> na agenda.</p>
                    <p>Em caso de dúvidas, sinalizar <a href="mailto:central.cbm@bistek.com.br" target="_blank">@central.cbm</a>.</p>
                    """

                elif qtd_semana == 0 and qtd_media > 0:

                    corpo = f"""
                    Boa dia/tarde,
                    <p>Após análise, verificamos que a loja citada (Loja <strong>{loja}</strong>) está com as baixas na agenda <strong><font size="4">{agenda} - {nome_agenda}</font></strong> <strong><font size="4" color="red">ZERADAS</font></strong>.</p>
                    <p>A <strong>média diária</strong> é de <strong><font size="4">R$ {round(qtd_media)}</font></strong>, e foram baixadas(os), <strong>nos últimos 7 dias</strong>, <strong>em média</strong> <strong><font size="4" color="red">R$ {round(qtd_semana)}</font></strong> por dia.</p>
                    <p><strong>Favor verificar de forma urgente</strong> se não <strong>deixaram de fazer alguma baixa na agenda</strong>.</p>
                    <p>Em caso de dúvidas, sinalizar <a href="mailto:central.cbm@bistek.com.br" target="_blank">@central.cbm</a>.</p>
                    """

                else:

                    print(f"[ {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} ] Loja {loja} sem dados. E-mail não enviado.")
                    continue
        
                destinatario = ','.join(emails)
                print(f"[ {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} ] Enviando e-mail para {destinatario}...")

                enviar_email(
                    service,
                    destinatario,
                    assunto,
                    corpo,
                    html=True
                )

if __name__ == "__main__":
    enviar_agendas_por_valor()