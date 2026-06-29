# -*- coding: utf-8 -*-
# codlines_nao.py - Python 2.7
# Ejecutar con: C:/Python27/python.exe codlines_nao.py <comando>

import sys
import time
from naoqi import ALProxy

# --- Configuracion de conexion ---
IP = "127.0.0.1"   # Simulador local
PROXY = 49609     # Puerto del simulador NAO

# --- Inicializar proxies ---
tts     = ALProxy("ALTextToSpeech", IP, PROXY)
postura = ALProxy("ALRobotPosture",  IP, PROXY)
motion  = ALProxy("ALMotion",        IP, PROXY)

# =============================================
#  ACCIONES
# =============================================

def saluda():
    """NAO saluda levantando el brazo y diciendo hola."""
    postura.goToPosture("StandInit", 0.7)
    time.sleep(0.3)

    # Levantar brazo derecho
    names  = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll"]
    angles = [-0.5, -0.3, 0.5]
    times  = [[1.0], [1.0], [1.0]]
    motion.angleInterpolation(names, angles, times, True)

    tts.say("Hola! Que tal estas?")
    time.sleep(0.5)

    # Volver postura inicial
    postura.goToPosture("StandInit", 0.7)


def baila():
    """NAO hace un baile simple: movimientos de brazos y torso."""
    postura.goToPosture("StandInit", 0.7)
    time.sleep(0.3)

    tts.say("A bailar!")
    time.sleep(0.3)

    # Secuencia de movimientos: brazos arriba/abajo alternados
    names_izq = ["LShoulderPitch", "LShoulderRoll"]
    names_der = ["RShoulderPitch", "RShoulderRoll"]

    for _ in range(3):
        motion.angleInterpolation(names_izq, [-0.5,  0.3], [[0.4], [0.4]], True)
        motion.angleInterpolation(names_der, [ 0.2, -0.3], [[0.4], [0.4]], True)
        motion.angleInterpolation(names_izq, [ 0.2,  0.1], [[0.4], [0.4]], True)
        motion.angleInterpolation(names_der, [-0.5, -0.1], [[0.4], [0.4]], True)

    tts.say("Eso es todo el show!")
    postura.goToPosture("StandInit", 0.7)


def sientate():
    """NAO se sienta usando la postura Sit."""
    tts.say("Me siento.")
    time.sleep(0.3)
    postura.goToPosture("Sit", 0.5)


# =============================================
#  DESPACHO DE COMANDOS
# =============================================

ACCIONES = {
    "saluda":    saluda,
    "baila":     baila,
    "sientate":  sientate,
    "siéntate":  sientate,   # con tilde por si Whisper la incluye
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python codlines_nao.py <comando>")
        print("Comandos disponibles:", list(ACCIONES.keys()))
        sys.exit(1)

    comando = sys.argv[1].lower().strip()

    if comando in ACCIONES:
        print("Ejecutando accion: " + comando)
        ACCIONES[comando]()
        print("Accion completada.")
    else:
        print("Comando desconocido: " + comando)
        print("Comandos disponibles: " + str(list(ACCIONES.keys())))
        sys.exit(2)
