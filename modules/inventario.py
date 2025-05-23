from my_lib import *

def inventarios():

    a = baixar_relatorio(1444).copy()
    a = string_repair(a, a.columns)
    a = float_repair(a, ['QTD_SIS', 'QTD_DIG', 'DIVERG', 'PENDENCIA', 'CUSTO', 'TOTAL_SIST', 'TOTAL_DIG', 'QTD_ULT_INV'])
    a = date_repair(a, ['DATA'])
    a['SECAO'] = a['COD_SEC'] + " - " + a['SECAO']
    a = a[['DATA', 'FILIAL', 'INVENTARIO', 'DEPARTAMENTO','SECAO', 'SKU', 'DESCRICAO', 'QTD_SIS', 'QTD_DIG', 'DIVERG', 'PENDENCIA', 'CUSTO', 'TOTAL_SIST']]
    a['DIVERG_REAL'] = (a['QTD_DIG'] + a['PENDENCIA']) - a['QTD_SIS']
    a['DIVERG_PERC'] = ((a['QTD_DIG'] + a['PENDENCIA']) / a['QTD_SIS']).fillna(1)
    a['TOTAL_SIST'] = a['CUSTO'] * a['DIVERG']
    a['TOTAL_SIST_REAL'] = a['CUSTO'] * a['DIVERG_REAL']
    a.replace([np.inf, -np.inf], np.nan, inplace=True)
    a.dropna(inplace=True)
    
    return a