# modules/__init__.py
from mailbot import *

from .inventario import inventarios
from .email import enviar_email_com_tabela
from .qbc import quebra_conhecida
from .pdf_creator import gerar_pdf