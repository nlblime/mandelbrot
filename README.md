# Mandelbrot – Interaktive Fraktal-Visualisierung (Python)

![Mandelbrot Screenshot](./docs/mandelbrot.png)

**Mandelbrot** rendert die Mandelbrot-Menge in Echtzeit mit **Numba** (JIT), **NumPy** und **Pygame**.  
Zoom, Pan und dynamische Iterationsanpassung sorgen für flüssige Exploration – bei extremen Zooms wird
automatisch auf **Decimal**-Arithmetik umgeschaltet, um Detailverlust zu vermeiden.

---

## 🚀 Features
- Echtzeit-Rendering mit **Numba**-Beschleunigung (`@njit`, `parallel=True`, `fastmath=True`)
- **Sanfte Farbverläufe** über sinus-basierte Palette (bis `max_farb_iter`)
- **Interaktive Steuerung**: Zoomen am Mauszeiger, Panning per Drag
- **Adaptive Iterationen**: `compute_max_iter(zoom)` skaliert mit dem Zoomlevel
- **Präzisionsmodus**: Automatischer Wechsel auf `decimal` ab sehr hohem Zoom

---

## 🎮 Steuerung

- **Mausrad:** Zoomen (zum Mauszeiger hin/weg)
- **Linke Maustaste halten + ziehen:** Panning/Verschieben
- **Pfeil ↑:** Basis-Iterationszahl verdoppeln (mehr Details)
- **Pfeil ↓:** Basis-Iterationszahl halbieren (schneller)
- **ESC oder Fenster schließen:** Beenden

---

## 🛠 Installation

> **Empfohlen:** Python **3.9** oder höher  
> Abhängigkeiten liegen in **`requirements.txt`**.

### 1️⃣ Repository klonen
```bash
git clone https://github.com/nlblime/mandelbrot.git
cd mandelbrot
```

### 2️⃣ Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### ▶️ Starten
```bash
python Mandelbrot.py
```
