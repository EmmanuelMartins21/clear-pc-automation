import os
import shutil
import ctypes
import time
from pathlib import Path
from datetime import datetime, timedelta

# CONFIGURAÇÕES
DIAS_LIMITE_DOWNLOADS = 30
LOG_DIR = Path("C:/RPA_Limpeza")
LOG_FILE = LOG_DIR / "limpeza_log.txt"

TEMP_USUARIO = os.getenv("TEMP")
TEMP_WINDOWS = r"C:\Windows\Temp"
DOWNLOADS = Path.home() / "Downloads"

# FUNÇÕES AUXILIARES
def admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def escrever_log(mensagem):
    LOG_DIR.mkdir(exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{datetime.now():%d/%m/%Y %H:%M:%S}] {mensagem}\n")

def limpar_pasta(caminho):
    for item in os.listdir(caminho):
        item_path = os.path.join(caminho, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
                escrever_log(f"Arquivo removido: {item_path}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                escrever_log(f"Pasta removida: {item_path}")
        except Exception as e:
            escrever_log(f"Erro ao remover {item_path} | {e}")

def executar_rpa():
    escrever_log("=== INÍCIO DA LIMPEZA AUTOMÁTICA ===")

    # Limpeza TEMP
    limpar_pasta(TEMP_USUARIO)
    limpar_pasta(TEMP_WINDOWS)
    escrever_log("Limpeza de arquivos temporários concluída")

    # Limpeza Downloads
    limite = datetime.now() - timedelta(days=DIAS_LIMITE_DOWNLOADS)

    for arquivo in DOWNLOADS.iterdir():
        if arquivo.is_file():
            data_mod = datetime.fromtimestamp(arquivo.stat().st_mtime)
            if data_mod < limite:
                try:
                    arquivo.unlink()
                    escrever_log(f"Download removido: {arquivo.name}")
                except Exception as e:
                    escrever_log(f"Erro ao remover download {arquivo.name} | {e}")

    escrever_log("=== FIM DA LIMPEZA ===\n")


if __name__ == "__main__": 
    if DEBBUG := True:
        executar_rpa()
    while True:
        executar_rpa()
        time.sleep(60 * 60 * 24)  # 1 vez por dia