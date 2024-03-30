"""Module implements music playback."""

from threading import Event
from pydub import AudioSegment
from pydub.playback import play, _play_with_simpleaudio
import pyaudio
from typing import Protocol


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
        self.p = pyaudio.PyAudio()
        self.last = 0

    def play(self, path: str, killPill: Event) -> None:
        """Play music."""
        try:
            music: Music = AudioSegment.from_mp3(path)
            # sample_width, frame_rate, channels, frame_width, _data
            self.stream = pyaudio.Stream(
                PA_manager=self.p,
                format=pyaudio.get_format_from_width(music.sample_width),
                channels=music.channels,
                rate=music.frame_rate,
                output=True
            )
            for i in range(self.last, len(music.raw_data), CHUNK):
                if killPill.is_set():
                    print('hertrr')
                    self.last = i
                    self.pause()
                    break
                self.stream.write(music.raw_data[i:i + CHUNK])
        except Exception:
            return

    def pause(self) -> None:
        self.stream.close()
        self.stream.stop_stream()
