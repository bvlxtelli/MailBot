from my_lib import *
from mailbot import *
from modules import gerar_pdf

x_dias = 45 # Dias
dias = timedelta(days=x_dias)
dsv = (hoje - dias)

def sem_venda(x):

    y = x

    y = date_repair(y, ['ULTIMAVENDA', 'DATA_INVENTARIO', 'DTULTENTRADA'])
    
    y = y.sort_values(
    
        by=['NOME_DPTO','NOME_SECAO','PRODUTO','DESCRICAO','LOJA'],
        ascending=[True, True, True, True, True]
    )

    y = y[
        (y['DATA_INVENTARIO'] < dsv ) &
        (y['ULTIMAVENDA'] < dsv ) &
        (y['DTULTENTRADA'] < dsv)
    ]

    return y

def enviar_sem_venda():

  service = login()
  
  for loja, emails in inventario_com_digito.items():
    
    titulo = f"SUSPEITO - SEM VENDA - LOJA {loja}"

    assunto = f'(URGENTE) {titulo}'
    corpo = f"Bom dia/tarde,\n\nSegue em anexo suspeito de produtos que estão há mais de {x_dias} dias sem venda na loja.\n\nEsse suspeito passa a ser semanal, ou seja, caso não seja feito irá acumular para a semana seguinte."

    print(f"Gerando PDF para loja {loja}...")
    
    pdf_buffer = gerar_pdf(base=sem_venda(baixar_relatorio(1217)), loja=loja, titulo=titulo)

    if pdf_buffer:
        
      nome_pdf = f"{titulo} - {datetime.now().strftime('%d-%m')}.pdf"
      destinatario = ','.join(['matheus.moura@bistek.com.br'])

      print(f"Enviando e-mail para {destinatario}...") 
        
      enviar_email(
        service,
        destinatario,
        assunto,
        corpo,
        caminho_anexo=None,
        anexo_buffer=pdf_buffer,
        nome_anexo=nome_pdf
      )

    else:
      
      print(f"Loja {loja} sem dados. E-mail não enviado.")

if __name__ == "__main__":
    enviar_sem_venda()