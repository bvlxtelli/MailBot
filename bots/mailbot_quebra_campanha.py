from utils import *
from mailbot import *

codigos_da_campanha = ["3060187", "2329395", "2329409", "2329468", "2329450", "2329441", "2329387", "2329417", "2329433", "2329425"]

def inventarios_campanha():

    x = inventarios()

    if dia_da_semana != 'Segunda':
        
        x = x[
            (x['DATA'] == ontem) &
            (x['SKU'].isin(codigos_da_campanha)) &
            (x['DIVERG'] != 0)
        ]
    
    else:
    
        x = x[
            (x['DATA'].isin([sexta, anteontem, ontem])) &
            (x['SKU'].isin(codigos_da_campanha)) &
            (x['DIVERG'] != 0)
        ]
    
    

    x = x[['DATA','FILIAL','INVENTARIO','DEPARTAMENTO','SECAO','SKU','DESCRICAO','QTD_SIS','QTD_DIG','PENDENCIA','DIVERG_REAL','TOTAL_SIST_REAL']]
    x.rename(columns={'TOTAL_SIST_REAL': 'DIVERG_R$'}, inplace=True)

    return x

def enviar_quebra_campanha():

    enviar_email_com_tabela(
        inventarios_campanha(),
        inventario_com_digito,
        "DIVERGÊNCIAS DE INV. - CAMPANHA",
        """<div>Bom dia/tarde,
        <br>
        <br>
        Após análise, identificamos <b>divergências</b> nos inventários da <b>campanha </b>na data citada. <b>Favor verificar de forma <font color="#ff0000">urgente</font></b><font color="#ff0000"> </font>e identificar o erro que ocorreu.
        </div>
        <br>
        """
    )

if __name__ == "__main__":
    enviar_quebra_campanha()