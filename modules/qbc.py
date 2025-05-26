from my_lib import *

def quebra_conhecida():

    x = baixar_relatorio(1262).copy()

    print(f"[ {pd.Timestamp.now()} ] Relatório baixado, filtrando o mesmo...")

    x = date_repair(x, ['DATA_FATURAMENTO', 'DATA_NOTIFICACAO'])
    x = string_repair(x, ['PRODUTO'])

    for col in ['CUSTO', 'CUSTO_TOTAL', 'QTD']:
        if not pd.api.types.is_float_dtype(x[col]):
            x[col] = x[col].astype(str).str.replace('[.]','', regex=True)
            x[col] = x[col].str.replace('[,]','.', regex=True).astype('float64')

    print(f"[ {pd.Timestamp.now()} ] Relatório criado")

    x = x[
        #(x['DATA_FATURAMENTO'] >= segunda_passada) &
        #(x['DATA_FATURAMENTO'] < hoje) &
        (x['AG'] == 531)
        ]

    print(f"[ {pd.Timestamp.now()} ] Relatório filtrado")

    return x