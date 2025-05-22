from my_lib import *
from mailbot import *

fornecedores = ['107123','173630','272850','84445','450200','460028','476536','481947']

quebra = [
    37869, 68519, 68594, 68640, 68659, 68667, 68900, 68934, 68985, 79952,
    83488, 83500, 83518, 83526, 83534, 83542, 87521, 87530, 94005, 95354,
    95397, 95460, 95478, 95486, 95494, 95508, 95516, 96130, 100455, 100463,
    100471, 100480, 100498, 105759, 108260, 108278, 108286, 108499, 109134,
    109142, 109185, 109193, 109207, 109215, 109223, 111015, 111023, 111031,
    111040, 114693, 115339, 115347, 115355, 116017, 116157, 116173, 116807,
    116815, 116823, 116831, 116858, 116866, 116874, 116882, 117447, 118826,
    118834, 118842, 118850, 118877, 118885, 118893, 118907, 118915, 118923,
    118931, 118940, 118982, 118990, 119008, 119016, 119024, 119032, 119040,
    119059, 119067, 119075, 119083, 119091, 119105, 119113, 119121, 119130,
    119148, 119156, 119164, 119172, 119180, 119199, 119202, 119385, 119393,
    119407, 119415, 119423, 119431, 119440, 119458, 119466, 119482, 119504,
    119512, 119520, 119539, 119547, 119555, 120030, 120049, 120057, 120065,
    120073, 120081, 120090, 120103, 120111, 120120, 120138, 120146, 120154,
    120162, 120170, 120189, 120219, 120235, 120243, 120251, 120260, 120995,
    121002, 121010, 121029, 121037, 121045, 121053, 121061, 121070, 121088,
    121096, 121100, 121118, 121126, 121134, 121142, 121150, 121169, 121177,
    121185, 121584, 121592, 121606, 122963, 122998, 123005, 123013, 123021,
    123030, 123048, 126055, 126063, 126080, 126101, 126110, 126128, 126187,
    126209, 127094, 127191, 127205, 127213, 127221, 127299, 127302, 127310,
    127329, 127337, 127345, 127353, 127663, 127671, 127698, 127701, 127710,
    127728, 127736, 127744, 128309, 128317, 128430, 132705, 132713, 132721,
    132756, 133302, 133310, 133329, 133337, 133345, 133353, 133361, 133370,
    133388, 133787, 133795, 133809, 133817, 133825, 133833, 133841, 133850,
    134953, 134996, 135003, 135011, 135020, 135593, 135607, 135615, 135623,
    135631, 135640, 136077, 136085, 136093, 137383, 137391, 137405, 137413,
    137421, 137430, 137448, 137456, 137502, 137510, 137529, 138258, 138266,
    138274, 138282, 1346490, 1508474, 1508571, 1630334, 1635123, 1635131,
    1635182, 1635263, 1639447, 1684540, 1740636, 1741713, 1778790, 1778820,
    1778927, 1778943, 1778951, 1778960, 1792962, 1792970, 1792997, 1793004,
    1827618, 1834096, 1947354, 2005930, 2005948, 2005956, 2005964, 2005972,
    2014920, 2026279, 2027313, 2027321, 2027330, 2049430, 2049457, 2049473,
    2049481, 2049490, 2049503, 2054582, 2064243, 2064251, 2064260, 2064278,
    2066025, 2071134, 2076276, 2080729, 2080737, 2119226, 2119390, 2148145,
    2148340, 2151146, 2151154, 2151162, 2151189, 2151189, 2151197, 2151200,
    2154838, 2154846, 2154854, 2154862, 2154870, 2154889, 2159490, 2161290,
    2161303, 2165392, 2165406, 2165414, 2165422, 2165430, 2165457, 2165465,
    2165473, 2165481, 2188201, 2188210, 2188228, 2188236, 2188244, 2188279,
    2190443, 2192721, 2192748, 2193841, 2193850, 2193868, 2193876, 2193884,
    2200538, 2200546, 2200554, 2200562, 2200570, 2210401, 2210410, 2210428,
    2210436, 2210444, 2210452, 2210460, 2210479, 2210614, 2221748, 2230038,
    2230046, 2239540, 2239558, 2239566, 2239574, 2239582, 2239590, 2239604,
    2239736, 2241137, 2241145, 2241153, 2241170, 2241188, 2241200, 2241218,
    2245159, 2245167, 2255626, 2255634, 2264021, 2264030, 2264048, 2264056,
    2282739, 2282747, 2282933, 2287900, 2295725, 2295750, 2295768, 2295776,
    2299100, 2299127, 2299135, 2299143, 2299151, 2299160, 2299178, 2299186,
    2302306, 2302373, 2302381, 2302390, 2302403, 2312620, 2312646, 2319535,
    2319543, 2319551, 3021696, 3021793, 3021840, 64181
]

def agendas(x,y):

    a = x.copy()

    a = a[a['AGENDA'] == 665]

    a['DT_AGENDA'] = pd.to_datetime(a['DT_AGENDA'], format='mixed', dayfirst=True)
    a['DT_AGENDA'] = a['DT_AGENDA'].dt.strftime('%d-%m-%Y')
    a['DT_AGENDA'] = pd.to_datetime(a['DT_AGENDA'], format='%d-%m-%Y', dayfirst=True)

    for col in ['VLR_TOTAL','VLR_NOTA','VL_CUSTO_NF','VL_CUSTO_TABELA','QUANTIDADE']:

        a[col] = a[col].astype(str).str.replace('[.]','', regex=True)
        a[col] = a[col].str.replace('[,]','.', regex=True).astype('float64')

    a['PRODUTO'] = a['PRODUTO'].str.replace('[-]','', regex=True).astype('int64')

    b = y.copy()

    b_filtro = ['RMS','CODIGO_FORNECEDOR','NOME_FORNECEDOR']

    b['CODIGO_FORNECEDOR'] = b['CODIGO_FORNECEDOR'].astype(str)
    b = b[b_filtro]
    b = b.rename(columns={'RMS': 'PRODUTO'})

    a = a.merge(b, on=['PRODUTO'], how='left')
    a = a.sort_values(by=['DT_AGENDA','VLR_TOTAL','DESCRICAO','NR_NOTA','NOME_FORNECEDOR'],ascending=False)
    a_filtro = ['CODIGO_FORNECEDOR','NOME_FORNECEDOR','PRODUTO','DESCRICAO','QUANTIDADE','VLR_TOTAL','AGENDA','FILIAL','NR_NOTA','DT_AGENDA']
    a = a[a_filtro]

    if dia_da_semana != 'Segunda':

        a = a[(a['DT_AGENDA'] == ontem) & (a['CODIGO_FORNECEDOR'].isin(fornecedores)) & (~a['PRODUTO'].isin(quebra))]
    
    else:

        a = a[((a['DT_AGENDA'] == ontem) | (a['DT_AGENDA'] == anteontem) | (a['DT_AGENDA'] == sexta) ) & (a['CODIGO_FORNECEDOR'].isin(fornecedores)) & (~a['PRODUTO'].isin(quebra))]

    return a

def enviar_qbc_troca_665():
    
    service = login()

    a = agendas(baixar_relatorio(274),baixar_relatorio(40))

    for loja, emails in ccp_sem_digito.items():
        
        print(f"[ {pd.Timestamp.now()} ] Gerando dados para loja {loja}...")

        dados_loja = a[a['FILIAL'] == loja]

        if not dados_loja.empty:

            tabela_html = dados_loja.to_html(index=False, justify='center', border=0, classes='tabela-pereciveis')
            tabela_html = tabela_html.replace(
            "<table>",
            """<table style="border-collapse:collapse;width:100%;font-family:Arial, sans-serif;font-size:14px">""")
            tabela_html = tabela_html.replace(
            "<th>",
            """<th style="text-align:center;padding:8px;border-bottom:2px solid #4682b4;background-color:#e6f2ff;color:#003366">""")
            tabela_html = tabela_html.replace(
            "<td>",
            """<td style="padding:6px;text-align:center;border-bottom:1px solid #ddd">""")

            titulo = f"TROCA LANÇADA NA QUEBRA - AGENDA 665 - LOJA {loja} - {ontem.strftime('%d/%m')}"
            assunto = f'{titulo}'
            
            corpo = f"""
            <p>Bom dia/tarde,</p>

            <p>Segue abaixo os lançamentos indevidos realizados na <strong>agenda 665</strong> no <strong>dia {ontem.strftime('%d/%m')}</strong> na Loja <strong>{loja}</strong>.</p>

            {tabela_html}

            <p>Favor verificar, pois são produtos <strong>troca que foram lançadas(os) na quebra de forma indevida</strong>.</p>

            <p>Em caso de dúvidas, sinalizar <a href="mailto:central.cbm@bistek.com.br" target="_blank">@central.cbm</a>.</p>
            """

            destinatario = ','.join(emails)
            print(f"[ {pd.Timestamp.now()} ] Enviando e-mail para {destinatario}...")

            enviar_email(
                service,
                destinatario,
                assunto,
                corpo,
                html=True
            )

        else:
            print(f"[ {pd.Timestamp.now()} ] Loja {loja} sem dados. E-mail não enviado.")

if __name__ == "__main__":
    
    enviar_qbc_troca_665()