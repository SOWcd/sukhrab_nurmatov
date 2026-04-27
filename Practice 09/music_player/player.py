import os
import wave
import contextlib
import pygame


class MusicPlayer:
    def __init__(self, playlist):
        if not playlist:
            raise ValueError("Playlist cannot be empty.")

        self.playlist = playlist
        self.current_index = 0
        self.is_playing = False
        self.is_stopped = True
        self.current_position = 0.0
        self.track_length = 0.0

        self._load_track()

    def _get_track_length(self, filepath):
        if filepath.lower().endswith(".wav"):
            try:
                with contextlib.closing(wave.open(filepath, "rb")) as audio_file:
                    frames = audio_file.getnframes()
                    rate = audio_file.getframerate()
                    if rate == 0:
                        return 0.0
                    return frames / float(rate)
            except (wave.Error, FileNotFoundError):
                return 0.0

        try:
            sound = pygame.mixer.Sound(filepath)
            return sound.get_length()
        except pygame.error:
            return 0.0

    def _load_track(self):
        current_track = self.playlist[self.current_index]
        pygame.mixer.music.load(current_track)
        self.track_length = self._get_track_length(current_track)
        self.current_position = 0.0

    def play(self):
        pygame.mixer.music.play()
        self.is_playing = True
        self.is_stopped = False
        self.current_position = 0.0

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_stopped = True
        self.current_position = 0.0

    def next_track(self):
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self._load_track()
        self.play()

    def previous_track(self):
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self._load_track()
        self.play()

    def update(self, dt):
        if self.is_playing:
            self.current_position += dt

            if self.track_length > 0 and self.current_position >= self.track_length:
                self.next_track()

    def get_current_track_name(self):
        return os.path.basename(self.playlist[self.current_index])

    def get_current_position(self):
        return self.current_position

    def get_current_track_length(self):
        return self.track_length

    def get_status(self):
        if self.is_playing:
            return "Playing"
        if self.is_stopped:
            return "Stopped"
        return "Paused"

    def cleanup(self):
        pygame.mixer.music.stop()