"""Module implements music playback."""
from typing import Protocol

from just_playback import Playback
import eyed3
from eyed3 import id3


class MusicMeta(Protocol):
    """Meta information from mp3."""

    title: str
    artist: str
    album: str
    images: id3.tag.ImagesAccessor
    album_artist: str
    composer: str
    publisher: str
    genre: str
    release_date: str


class Music(Protocol):
    """Audio properties."""

    sample_width: int
    frame_rate: int
    channels: int
    frame_width: int
    raw_data: bytes


CHUNK = 100000


class AudioPlayer:
    """Class to interact with audio."""

    def __init__(self) -> None:
        self.playback = None
        self.p = Playback()
        self.last = 0.
        self.__music_meta: MusicMeta | None = None

    @property
    def music_meta(self) -> MusicMeta:
        """Получить мета-информацию о текущей песне."""
        if self.__music_meta is None:
            raise Exception()
        return self.__music_meta

    @property
    def seconds_current_time(self) -> int:
        """Текущий тайминг музыки в секундах."""
        return int(self.p.curr_pos)

    @property
    def seconds_duration(self) -> int:
        """Длительность текущей песни в секундах."""
        return int(self.p.duration)

    @property
    def current_time(self) -> str:
        """Текущий тайминг времени в виде строки mm:ss."""
        minutes = int(self.p.curr_pos // 60)
        seconds = int(self.p.curr_pos - minutes * 60)
        return f'{str(minutes).zfill(2)}:{str(seconds).zfill(2)}'

    @property
    def duration(self) -> str:
        """Длительность текущей песни в виде строки mm:ss."""
        minutes = int(self.p.duration // 60)
        seconds = int(self.p.duration - minutes * 60)
        return f'{str(minutes).zfill(2)}:{str(seconds).zfill(2)}'

    def set_music_time(self, seconds: int) -> None:
        self.p.seek(seconds)
        self.last = seconds

    def play(self, path: str) -> None:
        """Начать проигрывание музыки."""
        try:
            if self.p.playing:
                return
            self.p.load_file(path)
            self.p.play()
            self.p.seek(self.last)
            self.__music_meta = eyed3.load(path).tag
        except Exception as e:
            print(e)
            return

    def pause(self) -> None:
        """Пауза музыки."""
        self.last = self.p.curr_pos
        self.p.pause()
