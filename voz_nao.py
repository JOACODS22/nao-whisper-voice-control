# -*- coding: utf-8 -*-
# voz_nao.py - Python 3
# Reconocimiento de voz con Whisper --> NAO
#
# Instalar dependencias (una sola vez):
#   pip install openai-whisper sounddevice scipy numpy
#   (en Windows también puede necesitar: pip install soundfile)

import time
import numpy as np
import sounddevice as sd
import whisper
from bridge_nao import enviar_comando_nao

# =============================================
#  CONFIGURACION
# =============================================

MODELO_WHISPER  = "base"        # tiny | base | small | medium | large
DURACION_GRAB   = 4             # segundos de escucha por ciclo
SAMPLE_RATE     = 16000         # Hz requerido por Whisper
IDIOMA          = "es"          # español

# Mapeo: fragmentos de texto --> comando NAO
# Whisper puede devolver variaciones; cubrimos las comunes
MAPA_COMANDOS = {
    "saluda":    "saluda",
    "salud":     "saluda",   # truncamiento posible
    "hola":      "saluda",
    "baila":     "baila",
    "bailar":    "baila",
    "siéntate":  "sientate",
    "sientate":  "sientate",
    "sienta":    "sientate",
    "sentarse":  "sientate",
}

# =============================================
#  FUNCIONES
# =============================================

def grabar_audio(duracion: int = DURACION_GRAB) -> np.ndarray:
    """Graba audio del micrófono y retorna array numpy float32."""
    print(f"\n🎙️  Escuchando... ({duracion}s) — Di: saluda | baila | siéntate")
    audio = sd.rec(
        int(duracion * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )
    sd.wait()
    return audio.flatten()


def transcribir(modelo, audio: np.ndarray) -> str:
    """Usa Whisper para transcribir el audio a texto."""
    resultado = modelo.transcribe(audio, language=IDIOMA, fp16=False)
    texto = resultado["text"].lower().strip()
    return texto


def detectar_comando(texto: str) -> str | None:
    """Busca en el texto transcrito si contiene algún comando conocido."""
    for palabra_clave, comando in MAPA_COMANDOS.items():
        if palabra_clave in texto:
            return comando
    return None


def bucle_principal():
    """Bucle infinito: escucha → transcribe → ejecuta."""
    print("=" * 50)
    print("  Sistema de voz para NAO  ")
    print(f"  Cargando modelo Whisper '{MODELO_WHISPER}'...")
    print("=" * 50)

    modelo = whisper.load_model(MODELO_WHISPER)
    print("✓ Modelo cargado.\n")
    print("Comandos disponibles: saluda | baila | siéntate")
    print("Presiona Ctrl+C para salir.\n")

    while True:
        try:
            audio   = grabar_audio()
            texto   = transcribir(modelo, audio)
            print(f"   Texto detectado: \"{texto}\"")

            comando = detectar_comando(texto)

            if comando:
                print(f"   ✓ Comando: {comando}")
                enviar_comando_nao(comando)
            else:
                print("   — No se detectó un comando válido.")

            time.sleep(0.5)

        except KeyboardInterrupt:
            print("\n\nSistema detenido por el usuario. ¡Hasta luego!")
            break
        except Exception as e:
            print(f"   ✗ Error en ciclo: {e}")
            time.sleep(1)


# =============================================
#  ENTRADA
# =============================================

if __name__ == "__main__":
    bucle_principal()
