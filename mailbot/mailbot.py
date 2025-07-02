import sys
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
import logging

logger = logging.getLogger(__name__)

# Escopos necessários para enviar e-mails.
SCOPES = [
  'https://mail.google.com/',
  'https://www.googleapis.com/auth/gmail.modify',
  'https://www.googleapis.com/auth/gmail.compose',
  'https://www.googleapis.com/auth/gmail.send'
]

BASE_DIR = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
TOKEN_PATH = os.path.join(BASE_DIR, 'dependencies', 'credentials', 'token.json') 
SECRET_PATH = os.path.join(BASE_DIR, 'dependencies', 'credentials', 'client_secret.json')

def login():
    logger.info("Iniciando o processo de login.")
    creds = None

    if os.path.exists(TOKEN_PATH):
        logger.debug(f"Token encontrado em {TOKEN_PATH}.")
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    else:
        logger.warning(f"Token não encontrado em {TOKEN_PATH}. Será necessário autenticar.")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Token expirado. Tentando renovar o token.")
            creds.refresh(Request())
            logger.debug("Token renovado com sucesso.")
        else:
            logger.info("Iniciando fluxo de autenticação.")
            flow = InstalledAppFlow.from_client_secrets_file(SECRET_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
            logger.debug("Autenticação concluída com sucesso.")

        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
            logger.debug(f"Novo token salvo em {TOKEN_PATH}.")

    logger.info("Login concluído com sucesso.")
    return build('gmail', 'v1', credentials=creds)

def criar_mensagem(destinatario, assunto, corpo, caminho_anexo=None, anexo_buffer=None, nome_anexo=None, multiplos_anexos=None, html=False):
    logger.info("Iniciando criação da mensagem.")
    mensagem = MIMEMultipart()
    mensagem['to'] = destinatario
    mensagem['subject'] = assunto
    logger.debug(f"Destinatário: {destinatario}, Assunto: {assunto}")

    tipo_conteudo = 'html' if html else 'plain'
    mensagem.attach(MIMEText(corpo, tipo_conteudo))
    logger.debug(f"Corpo do e-mail adicionado. Tipo: {tipo_conteudo}")

    if caminho_anexo and os.path.isfile(caminho_anexo):
        logger.debug(f"Anexo encontrado no caminho: {caminho_anexo}")
        nome_arquivo = os.path.basename(caminho_anexo)

        with open(caminho_anexo, 'rb') as f:
            mime_base = MIMEBase('application', 'octet-stream')
            mime_base.set_payload(f.read())
            encoders.encode_base64(mime_base)
            mime_base.add_header('Content-Disposition', f'attachment; filename="{str(Header(nome_arquivo, "utf-8"))}"')
            mensagem.attach(mime_base)
        logger.debug(f"Anexo {nome_arquivo} adicionado à mensagem.")

    elif anexo_buffer and nome_anexo:
        logger.debug(f"Anexo em buffer adicionado com o nome: {nome_anexo}")
        mime_base = MIMEBase('application', 'pdf')
        mime_base.set_payload(anexo_buffer.read())
        encoders.encode_base64(mime_base)
        mime_base.add_header('Content-Disposition', f'attachment; filename="{str(Header(nome_anexo, "utf-8"))}"')
        mensagem.attach(mime_base)
        anexo_buffer.seek(0)

    if multiplos_anexos:
        logger.debug(f"Adicionando múltiplos anexos. Total: {len(multiplos_anexos)}")
        for nome, buffer in multiplos_anexos.items():
            logger.debug(f"Adicionando anexo: {nome}")
            mime_base = MIMEBase('application', 'pdf')
            mime_base.set_payload(buffer.read())
            encoders.encode_base64(mime_base)
            mime_base.add_header('Content-Disposition', f'attachment; filename="{str(Header(nome, "utf-8"))}"')
            mensagem.attach(mime_base)
            buffer.seek(0)

    mensagem_bytes = mensagem.as_bytes()
    mensagem_base64 = base64.urlsafe_b64encode(mensagem_bytes).decode()
    logger.info("Mensagem criada com sucesso.")

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
  
  logger.info(f"E-mail enviado! ID da mensagem: {send_message['id']}")