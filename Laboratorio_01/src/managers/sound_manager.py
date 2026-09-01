"""
Gestor de audio: música y efectos de sonido.
"""
import os
import pygame


class SoundManager:
    def __init__(self, settings):
        self.settings = settings
        self.sounds = {}
        self.music_playing = False
        self._load_sounds()

    def _load_sounds(self):
        sound_files = {
            "shoot": "sfx/laser.wav",
            "explosion": "sfx/explosion.wav",
            "player_hit": "sfx/explosion.wav",
        }
        for key, relative_path in sound_files.items():
            full_path = os.path.join(self.settings.audio_dir, relative_path)
            if os.path.exists(full_path):
                try:
                    self.sounds[key] = pygame.mixer.Sound(full_path)
                except pygame.error:
                    self.sounds[key] = None
            else:
                self.sounds[key] = None

    def play(self, key, loops=0):
        sound = self.sounds.get(key)
        if sound:
            sound.play(loops)

    def play_music(self, filename, loops=-1, volume=0.5):
        music_path = os.path.join(self.settings.audio_dir, "music", filename)
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loops)
            self.music_playing = True

    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_playing = False
