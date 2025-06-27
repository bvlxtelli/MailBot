from .my_vars import *
import logging

# --- Logger ---------------------------------------------------------------------------------------

# Define BASE_DIR
#BASE_DIR = "/mnt/projeto_ia/CBM"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#BASE_DIR = os.getcwd()

# Cria a pasta Log
LOG_DIR = os.path.join(BASE_DIR, "log")
os.makedirs(LOG_DIR, exist_ok=True)

# Verifica se o arquivo de log existe, se não, cria
log_file_path = os.path.join(LOG_DIR, "log_thincake_request.log")
if not os.path.exists(log_file_path):
    with open(log_file_path, 'w') as log_file:
        log_file.write(f"[ {pd.Timestamp.now()} ] Arquivo de log criado.\n")

logging.basicConfig(
    level=logging.DEBUG,  # Nível mínimo de log
    format='[ %(asctime)s ] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "log_thincake_request.log")),  # Salva arquivo no dir de logs
        logging.StreamHandler()  # Mostra no console
    ]
)

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------------------------------