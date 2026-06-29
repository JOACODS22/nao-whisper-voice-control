# Control de Robot NAO por Voz con Whisper

Sistema de reconocimiento de voz que permite controlar un robot NAO mediante comandos hablados, usando OpenAI Whisper para la transcripción y NAOqi para el control del robot.

## Descripción

El micrófono de la laptop escucha comandos simples en español (*"saluda"*, *"baila"*, *"siéntate"*). Whisper convierte el audio a texto, el programa identifica el comando y lo envía al robot NAO, que ejecuta la acción correspondiente.

```
Micrófono (laptop) → Whisper (transcripción) → Comando → NAO (Choregraphe / robot físico)
```

## Arquitectura

El proyecto combina dos versiones de Python porque la librería oficial del NAO (`naoqi`) solo es compatible con Python 2.7, mientras que Whisper requiere Python 3.

| Archivo | Python | Función |
|---|---|---|
| `voz_nao.py` | 3.x | Escucha el micrófono, transcribe con Whisper, detecta el comando |
| `bridge_nao.py` | 3.x | Puente que ejecuta `codlines_nao.py` como subproceso |
| `codlines_nao.py` | 2.7 | Se conecta a NAOqi y ejecuta la acción en el robot |

## Requisitos

- Python 3.10+
- Python 2.7 con el SDK `pynaoqi` instalado
- Choregraphe (para pruebas con robot virtual) o un robot NAO físico
- ffmpeg

## Instalación

```bash
pip install openai-whisper sounddevice scipy numpy
```

## Uso

1. Conecta el robot virtual en Choregraphe (o conecta el NAO físico) y ajusta `IP` y `PROXY` en `codlines_nao.py`.
2. Ejecuta:
```bash
python voz_nao.py
```
3. Di en voz alta uno de los comandos disponibles: `saluda`, `baila`, `siéntate`.

También puedes probar sin usar el micrófono:
```bash
python bridge_nao.py saluda
```

## Evaluación del modelo

Se realizaron 30 pruebas (10 por comando) registradas en `evaluacion_nao.xlsx`. Las métricas (accuracy, F1-score, matriz de confusión) se calculan con:

```bash
python metricas_nao.py
```

### Resultados obtenidos

| Comando | Accuracy |
|---|---|
| saluda | 100% |
| baila | 60% |
| siéntate | 60% |
| **Global** | **73.3%** |

![Resultados](image.png)

## Limitaciones

- Latencia de ~12 segundos por comando (procesamiento de Whisper en CPU).
- El micrófono usado es el de la laptop, no el del robot NAO.
- Pruebas realizadas en ambiente con ruido de fondo.

## Mejoras futuras

- Usar el micrófono del propio NAO (`ALAudioDevice`) para mayor autonomía.
- Reducir la latencia usando un modelo Whisper más liviano o GPU.
- Ampliar el set de comandos reconocidos.

## Autores

Proyecto desarrollado como parte del curso de Inteligencia Artificial / UPC — 2026.

## Link del video

- [Ver video:](https://youtu.be/d8I83PWbM5w)



