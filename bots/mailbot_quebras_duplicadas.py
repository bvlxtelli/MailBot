from .__base__ import *

print(f"[ {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} ] Iniciando aplicação...")

def dpc():

    print(f"[ {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} ] Buscando relatório no Thincake...")

    x = quebra_conhecida()

    print(f"[ {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} ] Relatório criado")

    if dia_da_semana != 'Segunda':
        x = x[(x['DATA_FATURAMENTO'] == ontem)]
    else:
        x = x[(x['DATA_FATURAMENTO'] < hoje) & (x['DATA_FATURAMENTO'] >= sexta)]
    
    x['CONT_SES'] = x.groupby(['CODIGO', 'DESCRICAO', 'LOJA'])['CODIGO'].transform('count')

    return x
