from .__base__ import *

print(f"[ {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} ] Iniciando aplicação...")

def qbc(coluna=None, relacao=None, parametro=None, valor=None):

    print(f"[ {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} ] Buscando relatório no Thincake...")

    x = quebra_conhecida()

    print(f"[ {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} ] Relatório criado")

    if dia_da_semana != 'Segunda':
        x = x[(x['DATA_FATURAMENTO'] == ontem)]
    else:
        x = x[(x['DATA_FATURAMENTO'] < hoje) & (x['DATA_FATURAMENTO'] >= sexta)]

    if coluna is not None and relacao is not None:
        x = x[x[coluna].astype(str).isin(relacao)]
    
    if parametro is not None and valor is not None:
        x = x[x[parametro] > valor]
    
    x['SOMA_QTD'] = x.groupby(['FILIAL', 'COD_PROD'])['QTD'].transform('sum')
    x['SOMA_R$'] = x.groupby(['FILIAL', 'COD_PROD'])['CUSTO_TOTAL'].transform('sum')
    x = x[['FILIAL', 'COD_PROD', 'PRODUTO', 'SOMA_QTD', 'SOMA_R$']].drop_duplicates()
    x = x.sort_values(by='SOMA_R$', ascending=False)
    x.columns = ['FILIAL', 'CÓDIGO', 'PRODUTO', 'QTD', 'R$']

    return x

# Quebra zero - Padaria - SKUS
relacao_padaria = ["68756","77305","85006","98418","96130","119148","41734","96520","41823","41840","41645","498882","498890","100498","2005948","2005964","2005972",
    "100463","100480","111015","111023","111031","119504","118940","118982","119482","120081","120090","120111","119385","119393","119407","119415","119466"]
# Quebra zero -  Frios - Seções
relacao_frios = ["7","8","9","10","11","12","13","14","22","31","850","863","840","841","858"]
# Quebra zero -  Frutas secas - Seções
relacao_frutas_secas = ["805"]
# Quebra zero -  Ovos - Seções
relacao_ovos = ["816"]
# Troca - Ovos - SKUS
relacao_troca_ovos = ["2093057","2093065","2108704","2030128"]
# Acima de 12 unidades - Leite - Seção
relacao_leite = ["161"]
# Acima de 3kg - Açougue - Seção
relacao_acougue = ["823","158","159","827","157","903"]
# Acima de 12 unidades - Cerveja - SKUS
relacao_cerveja = ["68756", "77305", "85006", "98418", "96130", "119148", "41734", "96520", "41823", "41840", "41645", "498882","498890", "100498", "2005948", "2005964",
    "2005972", "100463", "100480", "111015", "111023", "111031","119504", "118940", "118982", "119482", "120081", "120090", "120111", "119385", "119393", "119407", "119415", 
    "119466", "991279", "990620", "990760", "990167", "990191", "990574", "997498", "997528", "997552", "997560","999288", "999296", "999008", "1322176", "1419420",
    "1433962", "1738070", "1943464", "1886746", "1886754", "2001926", "1948113"]

a = qbc(coluna='COD_PROD',relacao=relacao_padaria,parametro='QTD',valor=0)
b = qbc(coluna='COD_PROD',relacao=relacao_troca_ovos,parametro='QTD',valor=0)
c = qbc(coluna='COD_PROD',relacao=relacao_cerveja,parametro='QTD',valor=12)
d = qbc(coluna='NSECAO',relacao=relacao_frios,parametro='QTD',valor=0)
e = qbc(coluna='NSECAO',relacao=relacao_frutas_secas,parametro='QTD',valor=0)
f = qbc(coluna='NSECAO',relacao=relacao_ovos,parametro='QTD',valor=0)
g = qbc(coluna='NSECAO',relacao=relacao_leite,parametro='QTD',valor=12)
h = qbc(coluna='NSECAO',relacao=relacao_acougue,parametro='QTD',valor=3)

relatorios = {
    'QUEBRA ZERO - PADARIA': a,
    'OVOS - TROCA NA QUEBRA': b,
    'QUEBRA CONHECIDA - CERVEJAS': c,
    'QUEBRA ZERO - FRIOS': d,
    'QUEBRA ZERO - FRUTAS SECAS': e,
    'QUEBRA ZERO - OVOS': f,
    'QUEBRA CONHECIDA - LEITE':g,
    'QUEBRA CONHECIDA - ACOUGUE':h
    }

def enviar_quebras():

    for desc, tabela in relatorios.items():

        enviar_email_com_tabela(
            tabela,
            teste_jutiao,
            f"{desc}",
            """
            <div>Bom dia/tarde,
            <br><br>
            Teste Teste Teste
            </div>
            <br>
            """
        )

if __name__ == "__main__":
    enviar_quebras()