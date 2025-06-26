from ..my_lib import *

def quebra_conhecida():

    x = baixar_relatorio(1262).copy()

    print(f"[ {pd.Timestamp.now()} ] Relatório baixado, filtrando o mesmo...")

    x = repair_things(x, date=['DATA_FATURAMENTO', 'DATA_NOTIFICACAO'], string=['PRODUTO'])

    for col in ['CUSTO', 'CUSTO_TOTAL', 'QTD']:
        if not pd.api.types.is_float_dtype(x[col]):
            x = float_repair(x, [col])

    print(f"[ {pd.Timestamp.now()} ] Relatório criado")

    x = x[
        (x['AG'] == 531)
        ]

    print(f"[ {pd.Timestamp.now()} ] Relatório filtrado")

    return x