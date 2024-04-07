from threading import Thread, Event

from PyQt5.QtGui import QPixmap, QCloseEvent

from .audioplayer import AudioPlayer
from .interfaces.mainwindow import Ui_MainWindow

from PyQt5 import QtWidgets

# TODO: Сжимать изображение
# TODO: перемещение слайдера
# TODO: Кэширование музыки


class Player(QtWidgets.QMainWindow):
    def __init__(self):
        super(Player, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.play_button.clicked.connect(self._clicked_play_btn)
        self.ui.pause_button.clicked.connect(self._clicked_pause_btn)
        self.player = AudioPlayer()
        self.killPill = Event()
        self.currentTime = Thread(
            target=self.__loop_set_current_duration, args=(self.killPill,))

    def __loop_set_current_duration(self, killPill: Event):
        """В отдельном потоке постоянно обновляем\
            значение слайдера и тайминга песни."""
        while True:
            if killPill.is_set():
                break
            self._set_current_time()
            self._set_slidet_position(self.player.seconds_current_time)

    def _set_slidet_position(self, pos: int) -> None:
        self.ui.time_bar.setSliderPosition(pos)

    def _set_range(self, min: int, max: int):
        self.ui.time_bar.setRange(min, max)
        self._set_slidet_position(0)

    def _set_current_time(self):
        self.ui.currenttime_label.setText(self.player.current_time)

    def __set_song_duration(self) -> None:
        self.ui.songduration_label.setText(self.player.duration)

    def __set_song_name(self) -> None:
        self.ui.songname_label.setText(self.player.music_meta.title)

    def __set_song_image(self) -> None:
        image = self.player.music_meta.images[0]
        pixmap = QPixmap()
        pixmap.loadFromData(image.image_data)
        self.ui.songpicture_label.setPixmap(pixmap)

    def __create_audio_thread(self) -> Thread:
        return Thread(target=self.play_audio)

    def play_audio(self) -> None:
        self.player.play(
            'demos/Radiohead_-_Creep_48022418.mp3')
        if not self.currentTime.is_alive():
            self.currentTime.start()
        self.__set_song_duration()
        self.__set_song_image()
        self.__set_song_name()
        self.__set_artist_name()
        self._set_range(0, self.player.seconds_duration)

    def __set_artist_name(self) -> None:
        self.ui.artistname_label.setText(self.player.music_meta.artist)

    def _clicked_pause_btn(self) -> None:
        self.player.pause()

    def _clicked_play_btn(self) -> None:
        self.audio_thread = self.__create_audio_thread()
        self.audio_thread.start()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.killPill.set()
        return super().closeEvent(a0)
