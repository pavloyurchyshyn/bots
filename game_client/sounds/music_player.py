from pygame.mixer import Sound
from pygame.mixer import music as Music

import os
from settings.base import SOUNDS_FOLDER

# from settings.music_default_settings import DEFAULT_MUSIC_VOLUME, MUSIC_MUTED, MUSIC_VOLUME
# from common.save_and_load_json_config import get_common_config, save_common_config

FOLDER_WITH_BACK_MUSIC = os.path.join(SOUNDS_FOLDER, 'back_music')


class MusicPlayer:
    MIN_VOLUME = 0.0
    VOL_STEP = 0.1
    MAX_VOLUME = 1.0 + VOL_STEP

    FADE = 2000

    def __init__(self):
        self.music_set = None
        self.load_back_music_list()

        self.played_list = set()

        # settings = get_common_config()

        self._current_song = None
        self._current_song_path = None
        self._current_song_length = None

        self._volume_lvl = 0.8  # settings.get(MUSIC_VOLUME, DEFAULT_MUSIC_VOLUME)  # sound lvl from 0.0 to 1.0

        self._muted = 0  # settings.get(MUSIC_MUTED, 0)
        self._paused = 0

        Music.set_volume(self._volume_lvl)
        # self.save_settings()

    def get_music_pos(self):
        return Music.get_pos() / 1000  # seconds

    def update(self):
        if not Music.get_busy() and not self._muted and not self._paused:
            self.add_second_song()
            self.play_back_music()

    def play_next(self):
        if Music.get_busy():
            Music.unload()

        if not self._muted:
            self.add_second_song()
            self.play_back_music()

    def load_back_music_list(self):
        try:
            music_list = filter(lambda file: file.endswith('.mp3') or file.endswith('.wav'),
                                os.listdir(FOLDER_WITH_BACK_MUSIC))
            music_list = map(lambda music: os.path.abspath(os.path.join(FOLDER_WITH_BACK_MUSIC, music)), music_list)

            self.music_set = set(music_list)
        except FileNotFoundError:
            # TODO add log message
            self.music_set = set()

    def add_second_song(self):
        if not self.music_set:
            self.music_set = self.played_list.copy()
            self.played_list.clear()

        if not self.music_set:
            self._current_song_path = None
            return

        second_comp = self.music_set.pop()
        self.played_list.add(second_comp)
        self._current_song = os.path.basename(second_comp)
        self._current_song_path = second_comp

    # def save_settings(self):
    #     config = get_common_config()
    #     config[MUSIC_VOLUME] = self._volume_lvl
    #     config[MUSIC_MUTED] = self._muted
    #     save_common_config(config)

    def play_back_music(self):
        if self._current_song_path and not self._muted:
            Music.load(self._current_song_path)
            Music.play(fade_ms=MusicPlayer.FADE)
            self._current_song_length = Sound(self._current_song_path).get_length()

    def pause_unpause_music(self):
        self.resume_back_music() if self._paused else self.pause_back_music()

    def pause_back_music(self):
        Music.pause()
        self._paused = 1

    def resume_back_music(self):
        Music.unpause()
        self._paused = 0

    def stop_back_music(self):
        Music.stop()

    def add_volume(self):
        self._muted = 0
        if self._paused:
            self.resume_back_music()

        self._volume_lvl += self.VOL_STEP
        if self._volume_lvl > self.MAX_VOLUME:
            self._volume_lvl = self.MAX_VOLUME

        Music.set_volume(self._volume_lvl)
        # self.save_settings()

    def minus_volume(self):
        self._volume_lvl -= self.VOL_STEP
        if self._volume_lvl < self.MIN_VOLUME or self._volume_lvl < self.VOL_STEP:
            self._volume_lvl = self.MIN_VOLUME

        Music.set_volume(self._volume_lvl)
        # self.save_settings()

    def mute(self):
        self._muted = 1
        self.pause_back_music()
        # self.save_settings()

    def unmute(self):
        self._muted = 0
        self.resume_back_music()
        # self.save_settings()

    def busy(self):
        return Music.get_busy()

    @property
    def current_song(self):
        return self._current_song

    @staticmethod
    def load_sound(path):
        return Sound(os.path.join(SOUNDS_FOLDER, path))

    @property
    def volume(self):
        return self._volume_lvl

    @property
    def volume_stages(self):
        return (self.MAX_VOLUME - self.MIN_VOLUME) // self.VOL_STEP + 1

    @property
    def volume_stage(self):
        return int((self.MAX_VOLUME - self.MIN_VOLUME) // self.VOL_STEP * self._volume_lvl)

    @property
    def muted(self):
        return self._muted

    @property
    def song_length(self):
        return self._current_song_length

    def click_sound(self):
        click = Sound(os.path.join(SOUNDS_FOLDER, 'button_click.wav'))
        click.set_volume(0.2)
        click.play()


GLOBAL_MUSIC_PLAYER = MusicPlayer()
