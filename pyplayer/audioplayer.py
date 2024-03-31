"""Module implements music playback."""
from typing import Protocol, Any
from threading import Event
 
import eyed3
from eyed3 import id3
from pydub import AudioSegment
import pyaudio


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
        self.p = pyaudio.PyAudio()
        self.last = 0
        self.time = 0.

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
            audio_meta: MusicMeta = eyed3.load(path).tag
            # for img in audio_meta.images:
            #     typed_img: id3.frames.ImageFrame = img
            #     with open('test.jpg', 'wb') as f:
            #         f.write(typed_img.image_data)
            #         print('hereere')
            #     break
            # print(type(audio_meta.images))
            print(len(music.raw_data), len(music._data))
            for i in range(self.last, len(music.raw_data), CHUNK):
                if killPill.is_set():
                    self.last = i
                    self.pause()
                    break
                self.stream.write(music.raw_data[i:i + CHUNK])
        except Exception as e:
            print(e)
            return

    def pause(self) -> None:
        self.time = self.stream.get_time()
        print(self.stream.get_write_available())
        print(self.time)
        self.stream.close()
        self.stream.stop_stream()
