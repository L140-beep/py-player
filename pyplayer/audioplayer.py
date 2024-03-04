"""Module implements music playback."""

from pydub import AudioSegment
from pydub.playback import play


class AudioPlayer:
    """Class to interact with audio."""

    def play(self, path: str) -> None:
        """Play music."""
        music = AudioSegment.from_mp3(path)
        play(music)
