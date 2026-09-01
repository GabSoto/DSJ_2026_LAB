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
│   │   ├── backgrounds/     # Fondos del juego
│   │   ├── bullets/         # Balas (bullet.png)
│   │   ├── enemies/         # Enemigos (enemy.png)
│   │   ├── explosions/      # Explosiones (explosion.png)
│   │   └── player/          # Nave del jugador (player.png)
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

Coloca tus propios archivos de audio e imágenes en las carpetas correspondientes dentro de `assets/`. El juego usa superficies de color como respaldo si no encuentra un archivo.

### Archivos esperados

| Tipo | Ruta esperada |
|------|---------------|
| Nave jugador | `assets/images/player/player.png` |
| Enemigo | `assets/images/enemies/enemy.png` |
| Bala jugador | `assets/images/bullets/bullet.png` |
| Bala enemiga | `assets/images/bullets/bullet.png` |
| Explosión | `assets/images/explosions/explosion.png` |
| Fondo | `assets/images/backgrounds/background.jpg` |
| Música | `assets/audio/music/background.wav` |
| Disparo | `assets/audio/sfx/laser.wav` |
| Explosión | `assets/audio/sfx/explosion.wav` |
| Daño jugador | `assets/audio/sfx/player_hit.wav` |
| Fuente | `assets/fonts/pixel.ttf` |

## Personalización

Edita `src/settings.py` para ajustar velocidades, vidas, tamaño de pantalla, colores y otros parámetros del juego.
