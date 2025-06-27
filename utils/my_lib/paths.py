from .my_vars import *

titulo = "Paths"

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "cbmPanel"))

PATHS = {
    
    "root": os.path.join(BASE_DIR),

    "credentials": os.path.join(BASE_DIR, "credentials", "logins.json"),

    "database": os.path.join(BASE_DIR, "database"),
    "log": os.path.join(BASE_DIR, "log", "log.txt"),
    "log csv": os.path.join(BASE_DIR, "log", "log_csv.txt"),
    "relatorios": os.path.join(BASE_DIR, "relatorios"),

    "relatorios/admin": os.path.join(BASE_DIR, "relatorios", "admin"),
    "relatorios/central": os.path.join(BASE_DIR, "relatorios", "central"),
    "relatorios/inventario": os.path.join(BASE_DIR, "relatorios", "inventario"),
    "relatorios/cbm": os.path.join(BASE_DIR, "relatorios", "cbm"),
    "relatorios/prevencao": os.path.join(BASE_DIR, "relatorios", "prevencao"),
    "relatorios/outros": os.path.join(BASE_DIR, "relatorios", "outros"),
    
    "database/csv": os.path.join(BASE_DIR, "database", "csv"),
    "database/csv/suspeitos_backup": os.path.join(BASE_DIR, "database", "csv", "suspeitos_backup")
    
}

REL_PATHS = {}

for relatorio in relatorios:
    REL_PATHS[f"relatorio_{relatorio}"] = os.path.join(BASE_DIR, PATHS["database/csv"], f"relatorio_{relatorio}-{hj}.csv")

for extra in planilhas_extras:
    REL_PATHS[extra] = os.path.join(BASE_DIR, PATHS["database/csv"], f"{extra}.csv")

print(f"[ {pd.Timestamp.now()} ] Módulo {titulo} carregado")