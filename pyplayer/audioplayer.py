"""Module implements music playback."""
from typing import Protocol, Any
from threading import Event

from just_playback import Playback
import eyed3
from eyed3 import id3


class MusicMeta(Protocol):
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
        self.last = 0
        self.time = 0.

    @property
    def duration(self):
        return self.p.duration

    def play(self, path: str, killPill: Event) -> None:
        """Play music."""
        try:
            self.p.load_file(path)
            self.p.play()
            self.p.seek(self.last)
            audio_meta: MusicMeta = eyed3.load(path).tag
        except Exception as e:
            print(e)
            return

    def pause(self) -> None:
        self.last = self.p.curr_pos
        self.p.pause()
