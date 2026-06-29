# Requisitos del Sistema

Este proyecto necesita software que **no se instala con pip** porque corre fuera del entorno normal de Python 3. Aquí están todos los requisitos separados por tipo.

## 1. Python

| Versión | Uso | Dónde se usa |
|---|---|---|
| Python 3.10+ | Whisper, puente de comandos | `voz_nao.py`, `bridge_nao.py`, `metricas_nao.py` |
| Python 2.7 (32-bit) | Control del robot NAO | `codlines_nao.py` |

> Python 2.7 es obligatorio porque la librería `naoqi` de Aldebaran/SoftBank nunca fue actualizada a Python 3.

## 2. NAOqi SDK (pynaoqi)

- Versión usada: `pynaoqi-2.1.4.13-win32`
- Debe coincidir en arquitectura (32-bit / 64-bit) con tu Python 2.7
- Debe coincidir en versión con tu Choregraphe
- Se instala ejecutando el `.exe` del SDK y agregando la ruta del SDK al `sys.path` dentro de `codlines_nao.py`

## 3. Choregraphe

- Simulador oficial de NAO usado para las pruebas (robot virtual)
- Verificar puerto activo en: `Edit > Preferences > Virtual Robot`

## 4. ffmpeg

Requerido internamente por Whisper para procesar audio.

```bash
winget install ffmpeg
```

## 5. Dependencias de Python 3 (pip)

Ver `requirements.txt`. Se instalan con:

```bash
pip install -r requirements.txt
```

## 6. Sistema operativo probado

- Windows 10 / 11
