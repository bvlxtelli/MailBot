from .my_vars import *

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

login_page = "https://bapi.bistek.com.br/login"
dados_login = {
    'username':'juliano.tavares',
    'password':'@Palmeiras@@01'
}

headers = {'User-Agent': 'Mozilla/5.0',}

cookies = {'PHPSESSID': '_ga=GA1.1.523997259.1743016736; AdoptVisitorId=IzCsCNQFgY3BaADAJlMeUCGATAZvATgDYBmA+ADhgFMJrdkCSpcg; VtexRCMacIdv7=9fd34d86-68f6-47ac-b3dc-9876642b12fe; _gcl_au=1.1.1385671564.1744034336; vtex-search-anonymous=8ba149b405e244ca8c0ed00237b87c47; _fbp=fb.2.1744034337140.238777460431722269; _gcl_gs=2.1.k1$i1744659471$u21441960; _gcl_aw=GCL.1744659477.CjwKCAjw5PK_BhBBEiwAL7GTPUifFZxOpwFZrJmEJPNcYRJV-rVEfnfrJ78-otDzsyNcR2H6Tdvo_BoCXXcQAvD_BwE; AdoptConsent=N4Ig7gpgRgzglgFwgSQCIgFwgCYEMAsAZgKwAcAnAEwC0UUADAMzX6mH3W4TnGfeXcAjFADsEUqRAAaEADc48BAHsATsmyYQgwcSjF8AYyjV6lYoJa5shauQBsjctVIGIuiIUrlGRaSAQGhADKCCpwAHYA5pjhAK4ANvEySgAOCMjhACq4kTCYANogAFIAXgCyMAAaCgC2AGoAWn4GuACaqDVwUKgAnpl+QZX0AIIAHqQAEgCKANLxfgD6AOIwQQBWUCqEPegyABYlgkoAokE9MHtLfuGtSmCMdpkA6pSCIAC6yWkA8rEI2bkCp8QAYlOEYBBwukNFgUjNjrIAI55GSg8GQhB1CAqeBgzB2GSxFJ4JDYYYITSUUy8ej4aiCfCZQTkDCMUgYegiAB0xHo9CaAF8gA; _ga_LE22E2DJJ4=GS1.1.1744659477.2.0.1744660016.21.0.0; _ga_1HGH72T9S7=GS1.1.1744659482.2.1.1744660018.60.0.0; username=anVsaWFuby50YXZhcmVz|1744923051|8603bef0947be98fc92a0d0e6f35c15665d85870'}

session = requests.Session()
resposta = session.post(login_page, data=dados_login, verify=False)

# --- // ---

params_274 = {
    'condicao_12719': {(hoje - (timedelta(days=90))).strftime('%d/%m/%Y')},
    'condicao_12720': {ontem.strftime('%d/%m/%Y')},
    'condicao_12314': '',
    'condicao_12312': '656,151,659,653,160,159,599,665',
    'condicao_12315': '',
    'condicao_12316': '',
    'paginado': 'false'
}

params_1262 = {
    'condicao_12973': '',
    'condicao_12974': '',
    'condicao_13037': {(hoje - (timedelta(days=7))).strftime('%d/%m/%Y')},
    'condicao_13038': {ontem.strftime('%d/%m/%Y')},
    'condicao_12978': '',
    'condicao_11466': '',
    'condicao_12981': '',
    'condicao_13330': '',
    'condicao_13370': '',
    'paginado': 'false'
}

params_1416 = {
    'condicao_12466': '01/01/2023',
    'condicao_12467': '31/12/2026',
    'condicao_12471': '',
    'paginado': 'false'
}

params_1217 = {
    'condicao_11160': '',
    #'condicao_11155': '90',
    'condicao_11155': '45',
    #'condicao_11156':'77,153,156,242,243,339,349,358,359,381,520,521,522,523,524,535,536,537,538,539,540,541,542,544,545,546,547,548,549,550,551,553,554,555,556,558,559,560,561,562,563,564,565,566,567,568,569,570,571,572,573,574,575,576,577,578,579,590,592,595,596,598,599,643,644,645,687,688,695,780,782,906,907,908,909,910,911,912,913,914,916,917,918,919,920,921,922,923,924,928,930,931,942,943,944,947,948,949,950,951,952,953,954,955,990,991',
    'condicao_11156': '79,84,109,110,111,112,113,114,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,195,197,201,256,257,258,259,260,262,263,264,265,266,267,295,296,297,298,299,350,351,352,353,355,356,357,382,383,384,385,386,387,388,389,391,392,393,394,395,396,397,398,399,508,509,510,530,531,532,534,689,690,691,692,693,697,698,750,764,765,786,936,937,961,962,963,964,965,966,967,968,969,970,971,972,973,974,975,976,977,978,979,996,997,998,999',
    'condicao_11157': '', 
    'condicao_11158': '', 
    'paginado': 'false'
}

params_40 = {
    'paginado':'false'
}

def montar_parametros(y):

    params = [('condicao_11936', x) for x in y]
    params.extend([
        ('condicao_11937', ''),
        ('condicao_12097', ''),
        ('condicao_13119', ''),
        ('condicao_13118', ''),
        ('paginado', 'false'),
    ])

    return params

lojas_pt1 = [2, 4, 5, 6, 7, 9, 10, 11, 12, 14, 16, 17, 18, 19]
lojas_pt2 = [20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33]

params_1334_pt1 = montar_parametros(lojas_pt1)
params_1334_pt2 = montar_parametros(lojas_pt2)

_relatorios_cache = {}

def get_relatorio(x,y):

    num_relatorio = x
    relatorio = f"https://bapi.bistek.com.br/relatorio/{num_relatorio}/csv"

    print(f"""[ {pd.Timestamp.now()} ] Gerando relatório {num_relatorio}... """)

    if num_relatorio != 1334:

        response = requests.get(relatorio, headers=headers, cookies=cookies, params=y, verify=False)

        while response.status_code == 502:
            
            print(f"[ {pd.Timestamp.now()} ] Request Status: ERRO - {response.status_code} - Tentando novamente...")

            time.sleep(5)

            response = requests.get(relatorio, headers=headers, cookies=cookies, params=y, verify=False)
        
    else:

            response_pt1 = requests.get(relatorio, headers=headers, cookies=cookies, params=params_1334_pt1, verify=False)
            response_pt2 = requests.get(relatorio, headers=headers, cookies=cookies, params=params_1334_pt2, verify=False)

            while response_pt1.status_code == 502 or response_pt2.status_code == 502 :

                print(f"[ {pd.Timestamp.now()} ] Request Status: {response_pt1.status_code} & {response_pt2.status_code} | ERRO | Tentando novamente...")

                time.sleep(5)

                response_pt1 = requests.get(relatorio, headers=headers, cookies=cookies, params=params_1334_pt1, verify=False)
                response_pt2 = requests.get(relatorio, headers=headers, cookies=cookies, params=params_1334_pt2, verify=False)
        
            merged_content = response_pt1.content + response_pt2.content[67:]

            output = io.StringIO()
            output.write(merged_content.decode('utf-8'))

            output.seek(0)
    
    print(f"""[ {pd.Timestamp.now()} ] Relatório CSV gerado em buffer! ✅""")

    if num_relatorio != 1334:

        return StringIO(response.text)
    
    else:

        return output

def get_params(numero):
    
    return globals().get(f'params_{numero}', {})

def baixar_relatorio(x):

    print(f"""[ {pd.Timestamp.now()} ] Gerando relatório {x}... """)

    if x in _relatorios_cache:
        
        print(f"[ {pd.Timestamp.now()} ] Relatório {x} carregado do cache ✅")
        return _relatorios_cache[x]

    y = get_relatorio(x, get_params(x))
    y = pd.read_csv(y, delimiter=';')
    _relatorios_cache[x] = y

    print(f"[ {pd.Timestamp.now()} ] Relatório {x} baixado e armazenado em cache ✅")

    return y