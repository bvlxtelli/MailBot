from my_lib import *
from mailbot import *

print(f"[ {pd.Timestamp.now()} ] Iniciando aplicação...")
print(f"[ {pd.Timestamp.now()} ] Buscando relatório no Thincake...")

def qbc(df):

    df = repair_things(
        df=df,
        date=['DATA_FATURAMENTO', 'DATA_NOTIFICACAO'],
        string=['PRODUTO','NDEPTO']
        )

    for col in ['CUSTO', 'CUSTO_TOTAL', 'QTD']:
        df[col] = df[col].str.replace('[.]', '', regex=True)
        df[col] = df[col].str.replace('[,]', '.', regex=True).astype('float64')

    print(f"[ {pd.Timestamp.now()} ] Relatório criado")

    if dia_da_semana != 'Segunda':
        df = df[(df['DATA_FATURAMENTO'] == ontem)]
    else:
        df = df[(df['DATA_FATURAMENTO'] < hoje) & (df['DATA_FATURAMENTO'] >= sexta)]
    
    df = df[(df['AG'] == 531)]
    df['SOMA_QTD'] = df.groupby(['FILIAL', 'COD_PROD'])['QTD'].transform('sum')
    df['SOMA_R$'] = df.groupby(['FILIAL', 'COD_PROD'])['CUSTO_TOTAL'].transform('sum')
    df = df[['FILIAL', 'COD_PROD', 'PRODUTO', 'SOMA_QTD', 'SOMA_R$']].drop_duplicates()
    df = df.sort_values(by='SOMA_R$', ascending=False)
    df.columns = ['FILIAL', 'CÓDIGO', 'PRODUTO', 'QTD', 'R$']

    return df