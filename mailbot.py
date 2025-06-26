import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from email.utils import formataddr
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from utils import *

# Escopos necessários para enviar e-mails.
SCOPES = [
  'https://mail.google.com/',
  'https://www.googleapis.com/auth/gmail.modify',
  'https://www.googleapis.com/auth/gmail.compose',
  'https://www.googleapis.com/auth/gmail.send'
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(BASE_DIR, 'utils', 'credentials', 'token.json')
SECRET_PATH = os.path.join(BASE_DIR, 'utils', 'credentials', 'client_secret.json')

def login():
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(SECRET_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def criar_mensagem(destinatario, assunto, corpo, caminho_anexo=None, anexo_buffer=None, nome_anexo=None, multiplos_anexos=None, html=False):

    mensagem = MIMEMultipart()
    mensagem['to'] = destinatario
    mensagem['subject'] = assunto

    tipo_conteudo = 'html' if html else 'plain'
    mensagem.attach(MIMEText(corpo, tipo_conteudo))

    if caminho_anexo and os.path.isfile(caminho_anexo):
        
        nome_arquivo = os.path.basename(caminho_anexo)

        with open(caminho_anexo, 'rb') as f:

            mime_base = MIMEBase('application', 'octet-stream')
            mime_base.set_payload(f.read())
            encoders.encode_base64(mime_base)
            mime_base.add_header('Content-Disposition', f'attachment; filename="{str(Header(nome_arquivo, 'utf-8'))}"')
            mensagem.attach(mime_base)

    elif anexo_buffer and nome_anexo:

        mime_base = MIMEBase('application', 'pdf')
        mime_base.set_payload(anexo_buffer.read())
        encoders.encode_base64(mime_base)
        mime_base.add_header('Content-Disposition', f'attachment; filename="{str(Header(nome_anexo, 'utf-8'))}"')
        mensagem.attach(mime_base)
        anexo_buffer.seek(0)

    if multiplos_anexos:

        for nome, buffer in multiplos_anexos.items():

            mime_base = MIMEBase('application', 'pdf')
            mime_base.set_payload(buffer.read())
            encoders.encode_base64(mime_base)
            mime_base.add_header('Content-Disposition', f'attachment; filename="{str(Header(nome, 'utf-8'))}"')
            mensagem.attach(mime_base)
            buffer.seek(0)

    mensagem_bytes = mensagem.as_bytes()
    mensagem_base64 = base64.urlsafe_b64encode(mensagem_bytes).decode()

    return {'raw': mensagem_base64}

def enviar_email(service, destinatario, assunto, corpo, caminho_anexo=None, anexo_buffer=None, nome_anexo=None, multiplos_anexos=None, html=False):
  
  mensagem = criar_mensagem(
    destinatario=destinatario,
    assunto=assunto,
    corpo=corpo,
    caminho_anexo=caminho_anexo,
    anexo_buffer=anexo_buffer,
    nome_anexo=nome_anexo,
    multiplos_anexos=multiplos_anexos,
    html=html
)
  send_message = service.users().messages().send(userId='me', body=mensagem).execute()
  print(f"[ {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} ] E-mail enviado! ID da mensagem: {send_message['id']}")

def teste_email():
    
  service = login()

  enviar_email(
    service,
    "matheus.moura@bistek.com.br",
    "EMAIL TESTE - MAILBOT",
    "TESTE\nTESTE\nTESTE\nTESTE\nTESTE\nTESTE\n"
    )
  
teste_com_digito = {
    27: ['matheus.moura@bistek.com.br'],
    43: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    51: ['matheus.moura@bistek.com.br'],
    60: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    78: ['matheus.moura@bistek.com.br'],
    94: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    108: ['matheus.moura@bistek.com.br'],
    116: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    124: ['matheus.moura@bistek.com.br'],
    140: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    167: ['matheus.moura@bistek.com.br'],
    175: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    183: ['matheus.moura@bistek.com.br'],
    191: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    205: ['matheus.moura@bistek.com.br'],
    213: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    221: ['matheus.moura@bistek.com.br'],
    230: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    248: ['matheus.moura@bistek.com.br'],
    256: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    264: ['matheus.moura@bistek.com.br'],
    272: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    299: ['matheus.moura@bistek.com.br'],
    302: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    310: ['matheus.moura@bistek.com.br'],
    329: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    337: ['matheus.moura@bistek.com.br'],
}


teste_sem_digito = {
    2: ['matheus.moura@bistek.com.br'],
    4: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    5: ['matheus.moura@bistek.com.br'],
    6: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    7: ['matheus.moura@bistek.com.br'],
    9: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    10: ['matheus.moura@bistek.com.br'],
    11: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    12: ['matheus.moura@bistek.com.br'],
    14: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    16: ['matheus.moura@bistek.com.br'],
    17: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    18: ['matheus.moura@bistek.com.br'],
    19: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    20: ['matheus.moura@bistek.com.br'],
    21: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    22: ['matheus.moura@bistek.com.br'],
    23: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    24: ['matheus.moura@bistek.com.br'],
    25: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    26: ['matheus.moura@bistek.com.br'],
    27: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    29: ['matheus.moura@bistek.com.br'],
    30: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    31: ['matheus.moura@bistek.com.br'],
    32: ['daniel.santos@bistek.com.br', 'matheus.moura@bistek.com.br'],
    33: ['matheus.moura@bistek.com.br'],
}
  
inventario_com_digito = {
    27: ['cbm02@bistek.com.br', 'inventario02@bistek.com.br', 'prevencao02@bistek.com.br', 'central.cbm@bistek.com.br'],
    43: ['cbm04@bistek.com.br', 'inventario04@bistek.com.br', 'prevencao04@bistek.com.br', 'central.cbm@bistek.com.br'],
    51: ['cbm05@bistek.com.br', 'inventario05@bistek.com.br', 'prevencao05@bistek.com.br', 'central.cbm@bistek.com.br'],
    60: ['cbm06@bistek.com.br', 'inventario06@bistek.com.br', 'prevencao06@bistek.com.br', 'central.cbm@bistek.com.br'],
    78: ['cbm07@bistek.com.br', 'inventario07@bistek.com.br', 'prevencao07@bistek.com.br', 'central.cbm@bistek.com.br'],
    94: ['cbm09@bistek.com.br', 'inventario09@bistek.com.br', 'prevencao09@bistek.com.br', 'central.cbm@bistek.com.br'],
    108: ['cbm10@bistek.com.br', 'inventario10@bistek.com.br', 'prevencao10@bistek.com.br', 'central.cbm@bistek.com.br'],
    116: ['cbm11@bistek.com.br', 'inventario11@bistek.com.br', 'prevencao11@bistek.com.br', 'central.cbm@bistek.com.br'],
    124: ['cbm12@bistek.com.br', 'inventario12@bistek.com.br', 'prevencao12@bistek.com.br', 'central.cbm@bistek.com.br'],
    140: ['cbm14@bistek.com.br', 'inventario14@bistek.com.br', 'prevencao14@bistek.com.br', 'central.cbm@bistek.com.br'],
    167: ['cbm16@bistek.com.br', 'inventario16@bistek.com.br', 'prevencao16@bistek.com.br', 'central.cbm@bistek.com.br'],
    175: ['cbm17@bistek.com.br', 'inventario17@bistek.com.br', 'prevencao17@bistek.com.br', 'central.cbm@bistek.com.br'],
    183: ['cbm18@bistek.com.br', 'inventario18@bistek.com.br', 'prevencao18@bistek.com.br', 'central.cbm@bistek.com.br'],
    191: ['cbm19@bistek.com.br', 'inventario19@bistek.com.br', 'prevencao19@bistek.com.br', 'central.cbm@bistek.com.br'],
    205: ['cbm20@bistek.com.br', 'inventario20@bistek.com.br', 'prevencao20@bistek.com.br', 'central.cbm@bistek.com.br'],
    213: ['cbm21@bistek.com.br', 'inventario21@bistek.com.br', 'prevencao21@bistek.com.br', 'central.cbm@bistek.com.br'],
    221: ['cbm22@bistek.com.br', 'inventario22@bistek.com.br', 'prevencao22@bistek.com.br', 'central.cbm@bistek.com.br'],
    230: ['cbm23@bistek.com.br', 'inventario23@bistek.com.br', 'prevencao23@bistek.com.br', 'central.cbm@bistek.com.br'],
    248: ['cbm24@bistek.com.br', 'inventario24@bistek.com.br', 'prevencao24@bistek.com.br', 'central.cbm@bistek.com.br'],
    256: ['cbm25@bistek.com.br', 'inventario25@bistek.com.br', 'prevencao25@bistek.com.br', 'central.cbm@bistek.com.br'],
    264: ['cbm26@bistek.com.br', 'inventario26@bistek.com.br', 'prevencao26@bistek.com.br', 'central.cbm@bistek.com.br'],
    272: ['cbm27@bistek.com.br', 'inventario27@bistek.com.br', 'prevencao27@bistek.com.br', 'central.cbm@bistek.com.br'],
    299: ['cbm29@bistek.com.br', 'inventario29@bistek.com.br', 'prevencao29@bistek.com.br', 'central.cbm@bistek.com.br'],
    302: ['cbm30@bistek.com.br', 'inventario30@bistek.com.br', 'prevencao30@bistek.com.br', 'central.cbm@bistek.com.br'],
    310: ['cbm31@bistek.com.br', 'inventario31@bistek.com.br', 'prevencao31@bistek.com.br', 'central.cbm@bistek.com.br'],
    329: ['cbm32@bistek.com.br', 'inventario32@bistek.com.br', 'prevencao32@bistek.com.br', 'central.cbm@bistek.com.br'],
    337: ['cbm33@bistek.com.br', 'inventario33@bistek.com.br', 'prevencao33@bistek.com.br', 'central.cbm@bistek.com.br'],
}

inventario_sem_digito = {
    2: ['cbm02@bistek.com.br', 'inventario02@bistek.com.br', 'prevencao02@bistek.com.br', 'central.cbm@bistek.com.br'],
    4: ['cbm04@bistek.com.br', 'inventario04@bistek.com.br', 'prevencao04@bistek.com.br', 'central.cbm@bistek.com.br'],
    5: ['cbm05@bistek.com.br', 'inventario05@bistek.com.br', 'prevencao05@bistek.com.br', 'central.cbm@bistek.com.br'],
    6: ['cbm06@bistek.com.br', 'inventario06@bistek.com.br', 'prevencao06@bistek.com.br', 'central.cbm@bistek.com.br'],
    7: ['cbm07@bistek.com.br', 'inventario07@bistek.com.br', 'prevencao07@bistek.com.br', 'central.cbm@bistek.com.br'],
    9: ['cbm09@bistek.com.br', 'inventario09@bistek.com.br', 'prevencao09@bistek.com.br', 'central.cbm@bistek.com.br'],
    10: ['cbm10@bistek.com.br', 'inventario10@bistek.com.br', 'prevencao10@bistek.com.br', 'central.cbm@bistek.com.br'],
    11: ['cbm11@bistek.com.br', 'inventario11@bistek.com.br', 'prevencao11@bistek.com.br', 'central.cbm@bistek.com.br'],
    12: ['cbm12@bistek.com.br', 'inventario12@bistek.com.br', 'prevencao12@bistek.com.br', 'central.cbm@bistek.com.br'],
    14: ['cbm14@bistek.com.br', 'inventario14@bistek.com.br', 'prevencao14@bistek.com.br', 'central.cbm@bistek.com.br'],
    16: ['cbm16@bistek.com.br', 'inventario16@bistek.com.br', 'prevencao16@bistek.com.br', 'central.cbm@bistek.com.br'],
    17: ['cbm17@bistek.com.br', 'inventario17@bistek.com.br', 'prevencao17@bistek.com.br', 'central.cbm@bistek.com.br'],
    18: ['cbm18@bistek.com.br', 'inventario18@bistek.com.br', 'prevencao18@bistek.com.br', 'central.cbm@bistek.com.br'],
    19: ['cbm19@bistek.com.br', 'inventario19@bistek.com.br', 'prevencao19@bistek.com.br', 'central.cbm@bistek.com.br'],
    20: ['cbm20@bistek.com.br', 'inventario20@bistek.com.br', 'prevencao20@bistek.com.br', 'central.cbm@bistek.com.br'],
    21: ['cbm21@bistek.com.br', 'inventario21@bistek.com.br', 'prevencao21@bistek.com.br', 'central.cbm@bistek.com.br'],
    22: ['cbm22@bistek.com.br', 'inventario22@bistek.com.br', 'prevencao22@bistek.com.br', 'central.cbm@bistek.com.br'],
    23: ['cbm23@bistek.com.br', 'inventario23@bistek.com.br', 'prevencao23@bistek.com.br', 'central.cbm@bistek.com.br'],
    24: ['cbm24@bistek.com.br', 'inventario24@bistek.com.br', 'prevencao24@bistek.com.br', 'central.cbm@bistek.com.br'],
    25: ['cbm25@bistek.com.br', 'inventario25@bistek.com.br', 'prevencao25@bistek.com.br', 'central.cbm@bistek.com.br'],
    26: ['cbm26@bistek.com.br', 'inventario26@bistek.com.br', 'prevencao26@bistek.com.br', 'central.cbm@bistek.com.br'],
    27: ['cbm27@bistek.com.br', 'inventario27@bistek.com.br', 'prevencao27@bistek.com.br', 'central.cbm@bistek.com.br'],
    29: ['cbm29@bistek.com.br', 'inventario29@bistek.com.br', 'prevencao29@bistek.com.br', 'central.cbm@bistek.com.br'],
    30: ['cbm30@bistek.com.br', 'inventario30@bistek.com.br', 'prevencao30@bistek.com.br', 'central.cbm@bistek.com.br'],
    31: ['cbm31@bistek.com.br', 'inventario31@bistek.com.br', 'prevencao31@bistek.com.br', 'central.cbm@bistek.com.br'],
    32: ['cbm32@bistek.com.br', 'inventario32@bistek.com.br', 'prevencao32@bistek.com.br', 'central.cbm@bistek.com.br'],
    33: ['cbm33@bistek.com.br', 'inventario33@bistek.com.br', 'prevencao33@bistek.com.br', 'central.cbm@bistek.com.br'],
}

ccp_sem_digito = {
    2: ['cbm02@bistek.com.br', 'prevencao02@bistek.com.br', 'central.cbm@bistek.com.br'],
    4: ['cbm04@bistek.com.br', 'prevencao04@bistek.com.br', 'central.cbm@bistek.com.br'],
    5: ['cbm05@bistek.com.br', 'prevencao05@bistek.com.br', 'central.cbm@bistek.com.br'],
    6: ['cbm06@bistek.com.br', 'prevencao06@bistek.com.br', 'central.cbm@bistek.com.br'],
    7: ['cbm07@bistek.com.br', 'prevencao07@bistek.com.br', 'central.cbm@bistek.com.br'],
    9: ['cbm09@bistek.com.br', 'prevencao09@bistek.com.br', 'central.cbm@bistek.com.br'],
    10: ['cbm10@bistek.com.br', 'prevencao10@bistek.com.br', 'central.cbm@bistek.com.br'],
    11: ['cbm11@bistek.com.br', 'prevencao11@bistek.com.br', 'central.cbm@bistek.com.br'],
    12: ['cbm12@bistek.com.br', 'prevencao12@bistek.com.br', 'central.cbm@bistek.com.br'],
    14: ['cbm14@bistek.com.br', 'prevencao14@bistek.com.br', 'central.cbm@bistek.com.br'],
    16: ['cbm16@bistek.com.br', 'prevencao16@bistek.com.br', 'central.cbm@bistek.com.br'],
    17: ['cbm17@bistek.com.br', 'prevencao17@bistek.com.br', 'central.cbm@bistek.com.br'],
    18: ['cbm18@bistek.com.br', 'prevencao18@bistek.com.br', 'central.cbm@bistek.com.br'],
    19: ['cbm19@bistek.com.br', 'prevencao19@bistek.com.br', 'central.cbm@bistek.com.br'],
    20: ['cbm20@bistek.com.br', 'prevencao20@bistek.com.br', 'central.cbm@bistek.com.br'],
    21: ['cbm21@bistek.com.br', 'prevencao21@bistek.com.br', 'central.cbm@bistek.com.br'],
    22: ['cbm22@bistek.com.br', 'prevencao22@bistek.com.br', 'central.cbm@bistek.com.br'],
    23: ['cbm23@bistek.com.br', 'prevencao23@bistek.com.br', 'central.cbm@bistek.com.br'],
    24: ['cbm24@bistek.com.br', 'prevencao24@bistek.com.br', 'central.cbm@bistek.com.br'],
    25: ['cbm25@bistek.com.br', 'prevencao25@bistek.com.br', 'central.cbm@bistek.com.br'],
    26: ['cbm26@bistek.com.br', 'prevencao26@bistek.com.br', 'central.cbm@bistek.com.br'],
    27: ['cbm27@bistek.com.br', 'prevencao27@bistek.com.br', 'central.cbm@bistek.com.br'],
    29: ['cbm29@bistek.com.br', 'prevencao29@bistek.com.br', 'central.cbm@bistek.com.br'],
    30: ['cbm30@bistek.com.br', 'prevencao30@bistek.com.br', 'central.cbm@bistek.com.br'],
    31: ['cbm31@bistek.com.br', 'prevencao31@bistek.com.br', 'central.cbm@bistek.com.br'],
    32: ['cbm32@bistek.com.br', 'prevencao32@bistek.com.br', 'central.cbm@bistek.com.br'],
    33: ['cbm33@bistek.com.br', 'prevencao33@bistek.com.br', 'central.cbm@bistek.com.br'],
}

ccp_com_digito = {
    27: ['cbm02@bistek.com.br', 'prevencao02@bistek.com.br', 'central.cbm@bistek.com.br'],
    43: ['cbm04@bistek.com.br', 'prevencao04@bistek.com.br', 'central.cbm@bistek.com.br'],
    51: ['cbm05@bistek.com.br', 'prevencao05@bistek.com.br', 'central.cbm@bistek.com.br'],
    60: ['cbm06@bistek.com.br', 'prevencao06@bistek.com.br', 'central.cbm@bistek.com.br'],
    78: ['cbm07@bistek.com.br', 'prevencao07@bistek.com.br', 'central.cbm@bistek.com.br'],
    94: ['cbm09@bistek.com.br', 'prevencao09@bistek.com.br', 'central.cbm@bistek.com.br'],
    108: ['cbm10@bistek.com.br', 'prevencao10@bistek.com.br', 'central.cbm@bistek.com.br'],
    116: ['cbm11@bistek.com.br', 'prevencao11@bistek.com.br', 'central.cbm@bistek.com.br'],
    124: ['cbm12@bistek.com.br', 'prevencao12@bistek.com.br', 'central.cbm@bistek.com.br'],
    140: ['cbm14@bistek.com.br', 'prevencao14@bistek.com.br', 'central.cbm@bistek.com.br'],
    167: ['cbm16@bistek.com.br', 'prevencao16@bistek.com.br', 'central.cbm@bistek.com.br'],
    175: ['cbm17@bistek.com.br', 'prevencao17@bistek.com.br', 'central.cbm@bistek.com.br'],
    183: ['cbm18@bistek.com.br', 'prevencao18@bistek.com.br', 'central.cbm@bistek.com.br'],
    191: ['cbm19@bistek.com.br', 'prevencao19@bistek.com.br', 'central.cbm@bistek.com.br'],
    205: ['cbm20@bistek.com.br', 'prevencao20@bistek.com.br', 'central.cbm@bistek.com.br'],
    213: ['cbm21@bistek.com.br', 'prevencao21@bistek.com.br', 'central.cbm@bistek.com.br'],
    221: ['cbm22@bistek.com.br', 'prevencao22@bistek.com.br', 'central.cbm@bistek.com.br'],
    230: ['cbm23@bistek.com.br', 'prevencao23@bistek.com.br', 'central.cbm@bistek.com.br'],
    248: ['cbm24@bistek.com.br', 'prevencao24@bistek.com.br', 'central.cbm@bistek.com.br'],
    256: ['cbm25@bistek.com.br', 'prevencao25@bistek.com.br', 'central.cbm@bistek.com.br'],
    264: ['cbm26@bistek.com.br', 'prevencao26@bistek.com.br', 'central.cbm@bistek.com.br'],
    272: ['cbm27@bistek.com.br', 'prevencao27@bistek.com.br', 'central.cbm@bistek.com.br'],
    299: ['cbm29@bistek.com.br', 'prevencao29@bistek.com.br', 'central.cbm@bistek.com.br'],
    302: ['cbm30@bistek.com.br', 'prevencao30@bistek.com.br', 'central.cbm@bistek.com.br'],
    310: ['cbm31@bistek.com.br', 'prevencao31@bistek.com.br', 'central.cbm@bistek.com.br'],
    329: ['cbm32@bistek.com.br', 'prevencao32@bistek.com.br', 'central.cbm@bistek.com.br'],
    337: ['cbm33@bistek.com.br', 'prevencao33@bistek.com.br', 'central.cbm@bistek.com.br'],
}

teste_jutiao = {
    27: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    43: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    51: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    60: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    78: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    94: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    108: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    116: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    124: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    140: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    167: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    175: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    183: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    191: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    205: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    213: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    221: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    230: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    248: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    256: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    264: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    272: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    299: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    302: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    310: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    329: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
    337: ['matheus.moura@bistek.com.br', 'juliano.tavares@bistek.com.br', 'sebastiao.nobre@bistek.com.br'],
}

central_cbm = ['matheus.moura@bistek.com.br','daniel.santos@bistek.com.br','juliano.tavares@bistek.com.br']