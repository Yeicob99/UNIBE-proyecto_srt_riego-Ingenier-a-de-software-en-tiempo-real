# Sistema de Riego Automático en Tiempo Real (STR)

Este proyecto implementa, en **Python**, un prototipo del *Sistema de Riego Automático con Sensor de Humedad* descrito en la actividad. Cumple con módulos, tareas periódicas y manejo de fallos, y registra mediciones/eventos en **SQLite**.

> Requisitos temporales objetivo: lectura 1s (≤80ms), decisión (≤120ms), actuación (≤100ms), almacenamiento cada 5s (≤300ms), detección de fallos cada 2s (≤150ms).

## Estructura

```
proyecto_srt_riego/
├─ src/
│  ├─ main.py
│  ├─ config.py
│  ├─ sensors.py
│  ├─ controller.py
│  ├─ actuator.py
│  ├─ storage.py
│  ├─ supervisor.py
│  ├─ scheduler.py
│  └─ utils.py
├─ tests/
│  └─ test_logic.py
├─ scripts/
│  └─ run.sh
├─ requirements.txt
├─ .gitignore
└─ README.md
```

## Requisitos
- Python 3.10+
- No requiere paquetes externos; usa la biblioteca estándar.

## Cómo ejecutar

```bash
python -m venv .venv && source .venv/bin/activate
python src/main.py
```

El programa crea `data/str.db` y logs en consola. Detén con `Ctrl+C`.

## Pruebas
```bash
python -m pytest -q
```

## Parámetros
Ajusta umbrales, frecuencias y *deadlines* en `src/config.py`.
