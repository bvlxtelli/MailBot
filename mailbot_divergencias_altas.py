from my_lib import *
from mailbot import *
from modules import inventarios, enviar_email_com_tabela

def inventarios_altos():

    x = inventarios()
    if dia_da_semana != 'Segunda':
        
        x = x[
            (
            (x['DATA'] == ontem) &
            (x['DIVERG_PERC'] > 1.75) &
            (x['TOTAL_SIST'] > 500)
            )
            |
            (x['TOTAL_SIST'] > 1000)
        ]
    
    else:
    
        x = x[
            (
            (x['DATA'].isin([sexta, anteontem, ontem])) &
            ((x['DIVERG_PERC'] > 1.80) | (x['DIVERG_PERC'] < 0.80)) &
            (x['TOTAL_SIST'] > 1000)
            )
            |
            (x['TOTAL_SIST'] > 1000)
        ]

    x = x[['DATA','FILIAL','INVENTARIO','DEPARTAMENTO','SECAO','SKU','DESCRICAO','QTD_SIS','QTD_DIG','PENDENCIA','DIVERG_REAL','TOTAL_SIST_REAL']]
    x.rename(columns={'TOTAL_SIST_REAL': 'DIVERG_R$'}, inplace=True)

    ['DATA','SOLICITADO','SUSPEITO','FILIAL','CODIGO']

    susp = pd.DataFrame({
    'DATA': datetime.now().strftime('%d-%m-%Y'),
    'SOLICITADO': 'MAILBOT',
    'SUSPEITO': 'DIVERGENCIAS ALTAS',
    'FILIAL': x['FILIAL'],
    'CODIGO': x['SKU']
    })

    susp.to_csv(REL_PATHS['db suspeitos'], mode='a', header=not pd.io.common.file_exists(REL_PATHS['db suspeitos']), index=False, sep=';')

    return x

def enviar_divergencias_altas():

    enviar_email_com_tabela(
        inventarios_altos(),
        inventario_com_digito,
        "SUSPEITO - DIVERGÊNCIAS DE INV. ALTAS",
        """
        <div>Bom dia/tarde,
        <br><br>
        Após análise, identificamos&nbsp;<b>divergências<font color="#ff0000"> altas</font></b>&nbsp;nos inventários <b>abaixo&nbsp;</b>na data citada.&nbsp;<b>Favor verificar de forma&nbsp;<font color="#ff0000">urgente</font></b><font color="#ff0000">&nbsp;</font>e identificar se ocorreu algum erro de processo e/ou contagem.
        </div>
        <br>
        """
    )

if __name__ == "__main__":
    enviar_divergencias_altas()