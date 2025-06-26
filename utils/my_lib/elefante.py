"""
Script para Configuração de Logs com RotatingFileHandler

Este script configura um sistema de logs para registrar mensagens de depuração, avisos e erros de uma aplicação. 
Os logs são salvos em arquivos rotativos e também exibidos no terminal, utilizando o formato e configurações definidos.

Principais Funcionalidades:
1. Configuração de logs em arquivos rotativos com níveis diferentes (DEBUG, WARNING).
2. Exibição de mensagens no terminal para facilitar o monitoramento.
3. Criação de novos loggers específicos para módulos ou funcionalidades.

Requisitos:
- Diretório base para logs (`/tmp/projeto_ia`) é criado automaticamente, caso não exista.
- Utiliza a biblioteca padrão `logging` para manipulação de logs.
- Permite que cada módulo ou funcionalidade tenha seu próprio arquivo de log.

Dependências:
- `dotenv`: Para carregar variáveis de ambiente.
"""



import logging
from logging import Formatter, StreamHandler
from logging.handlers import RotatingFileHandler
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

FORMATO_SINTAXE = (
    "(%(levelname)s) [%(asctime)s "
    "%(name)s:%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
)
FORMATO_DH = "%y%m%d %H:%M:%S"
FORMATO = Formatter(FORMATO_SINTAXE, datefmt=FORMATO_DH)
RAIZ = Path("/tmp/projeto_ia")
RAIZ = Path(r'\\qlik.bistek.com.br\Projeto-IA\Dados_parquet')
if not RAIZ.exists():
    RAIZ.mkdir()

log_root = logging.getLogger()
log_root.setLevel(logging.DEBUG)
arquivo_rotativo = RotatingFileHandler(
    f"{RAIZ}/avisos.log",
    encoding="utf8",
    maxBytes=50 * 1024 * 1024,
    backupCount=5,
)
arquivo_rotativo.setLevel(logging.WARNING)
arquivo_rotativo.setFormatter(FORMATO)
arquivo_debug = RotatingFileHandler(
    f"{RAIZ}/debug.log",
    encoding="utf8",
    maxBytes=50 * 1024 * 1024,
    backupCount=5,
)
arquivo_debug.setLevel(logging.DEBUG)
arquivo_debug.setFormatter(FORMATO)
terminal = StreamHandler()
terminal.setLevel(logging.DEBUG)
terminal.setFormatter(FORMATO)
log_root.addHandler(arquivo_rotativo)
log_root.addHandler(arquivo_debug)
log_root.addHandler(terminal)


def log_novo(nome: str) -> logging.Logger:
    """
    Descrição de como a função funciona:
    Cria e configura um novo logger para registrar logs específicos de um módulo ou funcionalidade. 
    Os logs são armazenados em um arquivo rotativo e exibidos no terminal.

    Args:
        nome (str): Nome do logger, que será usado também como nome do arquivo de log.

    Returns:
        logging.Logger: Logger configurado para registrar mensagens em um arquivo dedicado.

    Observações:
        - O arquivo de log criado estará localizado no diretório `/tmp/projeto_ia`.
        - As mensagens são formatadas utilizando a sintaxe especificada no formato global `FORMATO`.
        - Certifique-se de que o nome do logger não contém caracteres inválidos para nomes de arquivos.
    """

    log = logging.getLogger(nome)
    log.setLevel(logging.DEBUG)
    handler = RotatingFileHandler(
        f"{RAIZ}/{nome.replace('.', '_')}.log",
        encoding="utf8",
        maxBytes=50 * 1024 * 1024,
        backupCount=5,
    )
    handler.setFormatter(FORMATO)
    log.addHandler(handler)
    return log
