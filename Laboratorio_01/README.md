# Space Invaders - Pygame

Juego tipo Space Invaders desarrollado con Python y Pygame.

## Estructura del proyecto

```
Laboratorio_01/
├── main.py                  # Punto de entrada del juego
├── requirements.txt         # Dependencias
├── README.md                # Este archivo
├── assets/                  # Recursos multimedia
│   ├── images/
│   │   ├── spacerage/       # Pack Space Rage (Player, Enemies, Explosions, FX, BG)
│   │   ├── backgrounds/     # Fondo de respaldo
│   │   ├── bullets/         # Balas de respaldo
│   │   ├── enemies/         # Enemigos de respaldo
│   │   ├── explosions/      # Explosiones de respaldo
│   │   └── player/          # Nave de respaldo
│   ├── audio/
│   │   ├── music/           # Música de fondo (background.wav)
│   │   └── sfx/             # Efectos de sonido
│   │       ├── laser.wav
│   │       ├── explosion.wav
│   │       └── player_hit.wav
│   └── fonts/               # Fuentes personalizadas (pixel.ttf)
└── src/                     # Código fuente
    ├── settings.py          # Configuración global
    ├── utils.py             # Utilidades
    ├── game.py              # Controlador principal
    ├── entities/            # Entidades del juego
    │   ├── player.py
    │   ├── enemy.py
    │   ├── bullet.py
    │   └── explosion.py
    ├── managers/            # Gestores
    │   ├── asset_manager.py
    │   ├── sound_manager.py
    │   └── enemy_manager.py
    └── screens/             # Pantallas
        ├── base_screen.py
        ├── menu_screen.py
        ├── game_screen.py
        └── game_over_screen.py
```

## Instalación

1. Crea un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
venv\Scripts\activate
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Cómo jugar

```bash
python main.py
```

### Controles

- **Flechas izquierda/derecha** o **A/D**: Mover la nave
- **ESPACIO**: Disparar
- **ENTER/ESPACIO** en menú: Iniciar juego
- **R** en game over: Reintentar
- **M** en game over: Volver al menú
- **ESC**: Salir

## Assets

Los sprites del juego salen del pack **Space Rage** (Artur Dycha, [dycha.net](http://dycha.net/)), copiado en `assets/images/spacerage/`. `AssetManager` carga esos PNG recortados (no hace falta el spritesheet). Si faltan, usa las imágenes viejas de `assets/images/` o un color sólido.

| Tipo | Ruta SpaceRage |
|------|----------------|
| Nave jugador | `spacerage/Player/player_b_*.png` |
| Enemigo | `spacerage/Enemies/enemy_1_*.png` |
| Enemigo especial | `spacerage/Enemies/enemy_2_*.png` |
| Mina | `spacerage/Enemies/mine_1_*.png` |
| Bala jugador | `spacerage/FX/vulcan_1.png` |
| Bala enemiga | `spacerage/FX/plasma_1.png` |
| Explosión | `spacerage/Explosions/explosion_1_*.png` |
| Fondo | `spacerage/BG.png` |
| Música | `assets/audio/music/background.wav` |
| Disparo | `assets/audio/sfx/laser.wav` |
| Explosión (sfx) | `assets/audio/sfx/explosion.wav` |
| Fuente | `assets/fonts/pixel.ttf` |

## Personalización

Edita `src/settings.py` para ajustar velocidades, vidas, tamaño de pantalla, colores y otros parámetros del juego.
