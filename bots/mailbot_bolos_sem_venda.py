from .__base__ import *

def bolos_sem_venda():

    a = baixar_relatorio(
        1217,
        SECAO=100,
        DIAS_SEM_VENDA=10
        )
    
    a.to_csv(f"C:\\Users\\Usuario\\Downloads\\invs_-_{hj}.csv", sep=';', index=False, encoding='utf-8-sig', float_format='%.2f')

    a = date_repair(a,['DATA_INVENTARIO','DTULTENTRADA'])
    a = a[(a['DESCRICAO'].str.contains("bolo", case=False, na=False)) & (a['DATA_INVENTARIO'] < (hoje - (timedelta(days=3)))) & (a['DTULTENTRADA'] < (hoje - (timedelta(days=10))))]
    a = a[['NOME_DPTO','NOME_SECAO','PRODUTO','DESCRICAO','LOJA']]

    susp = pd.DataFrame({
    'DATA': datetime.now().strftime('%d-%m-%Y'),
    'SOLICITADO': 'MAILBOT',
    'SUSPEITO': 'ITENS SEM VENDA - BOLOS',
    'FILIAL': a['LOJA'],
    'CODIGO': a['PRODUTO']
    })

    susp.to_csv(REL_PATHS['db suspeitos'], mode='a', header=not pd.io.common.file_exists(REL_PATHS['db suspeitos']), index=False, sep=';')

    return a

def enviar_bolos_sem_venda():

    enviar_email_com_tabela(
        bolos_sem_venda(),
        inventario_com_digito,
        "(URGENTE) SUSPEITO - BOLOS SEM VENDA",
        """
        <div>Bom dia/tarde,
        <br><br>
        Após análise, encontramos estes SKUs de bolos que estão&nbsp;<b>sem venda</b>&nbsp;na loja nos&nbsp;<b>últimos 10 dias</b>.&nbsp;<b>Favor verificar de forma&nbsp;<font color="#ff0000">urgente</font></b>.
        </div>
        <br>
        """,
        filial_ou_loja='loja'
    )

if __name__ == "__main__":
    enviar_bolos_sem_venda()