# -*- coding: utf-8 -*-
# bridge_nao.py - Python 3
# Puente entre Python 3 y el script NAO en Python 2.7

import subprocess
import time
import sys

PYTHON27_PATH = "C:/Python27/python.exe"
SCRIPT_NAO    = "codlines_nao.py"

COMANDOS_VALIDOS = ["saluda", "baila", "sientate"]


def enviar_comando_nao(comando: str) -> bool:
    """
    Llama al script Python 2.7 con el comando dado.
    Retorna True si el NAO ejecutó la acción correctamente.
    """
    comando = comando.lower().strip()

    # Normalizar: quitar tilde por consistencia
    if comando == "siéntate":
        comando = "sientate"

    if comando not in COMANDOS_VALIDOS:
        print(f"[Bridge] Comando no reconocido: '{comando}'")
        print(f"[Bridge] Comandos válidos: {COMANDOS_VALIDOS}")
        return False

    print(f"[Bridge] Enviando comando al NAO: '{comando}'")
    start = time.time()

    try:
        result = subprocess.run(
            [PYTHON27_PATH, SCRIPT_NAO, comando],
            capture_output=True,
            text=True,
            timeout=30
        )

        elapsed = round(time.time() - start, 2)

        if result.returncode == 0:
            print(f"[Bridge] ✓ Ejecutado en {elapsed}s")
            if result.stdout:
                print(f"[Bridge] NAO dice: {result.stdout.strip()}")
            return True
        else:
            print(f"[Bridge] ✗ Error (código {result.returncode}) en {elapsed}s")
            if result.stderr:
                print(f"[Bridge] stderr: {result.stderr.strip()}")
            return False

    except subprocess.TimeoutExpired:
        print("[Bridge] ✗ Timeout: el NAO tardó demasiado.")
        return False
    except FileNotFoundError:
        print(f"[Bridge] ✗ No se encontró Python 2.7 en: {PYTHON27_PATH}")
        print("         Verifica la ruta en la variable PYTHON27_PATH.")
        return False
    except Exception as e:
        print(f"[Bridge] ✗ Error inesperado: {e}")
        return False


# --- Uso directo desde línea de comandos ---
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        cmd = sys.argv[1]
        exito = enviar_comando_nao(cmd)
        sys.exit(0 if exito else 1)
    else:
        print("Uso: python bridge_nao.py <comando>")
        print(f"Comandos: {COMANDOS_VALIDOS}")
