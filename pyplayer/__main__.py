"""Main module."""

import sys
from threading import Thread, Event

from PyQt5.QtGui import QPixmap, QCloseEvent

from .audioplayer import AudioPlayer
from .interfaces.mainwindow import Ui_MainWindow

from PyQt5 import QtWidgets


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.play_button.clicked.connect(self.clickedPlayBtn)
        self.ui.pause_button.clicked.connect(self.clickedPauseBtn)
        self.player = AudioPlayer()
        self.killPill = Event()
        self.currentTime = Thread(
            target=self.loopSettingCurrentDuration, args=(self.killPill,))

    def loopSettingCurrentDuration(self, killPill: Event):
        while True:
            if killPill.is_set():
                break
            self.setCurrentTime()
            self.setSliderPosition(self.player.seconds_current_time)

    def setSliderPosition(self, pos: int) -> None:
        self.ui.time_bar.setSliderPosition(pos)

    def setRange(self, min: int, max: int):
        self.ui.time_bar.setRange(min, max)
        self.setSliderPosition(0)

    def setCurrentTime(self):
        self.ui.currenttime_label.setText(self.player.current_time)

    def setSongDuration(self) -> None:
        self.ui.songduration_label.setText(self.player.duration)

    def setSongName(self) -> None:
        self.ui.songname_label.setText(self.player.music_meta.title)

    def setSongImage(self) -> None:
        image = self.player.music_meta.images[0]
        pixmap = QPixmap()
        pixmap.loadFromData(image.image_data)
        self.ui.songpicture_label.setPixmap(pixmap)

    def createAudioThread(self) -> Thread:
        return Thread(target=self.playAudio)

    def playAudio(self) -> None:
        self.player.play(
            'demos/Radiohead_-_Creep_48022418.mp3')
        if not self.currentTime.is_alive():
            self.currentTime.start()
        self.setSongDuration()
        self.setSongImage()
        self.setSongName()
        self.setArtistName()
        self.setRange(0, self.player.seconds_duration)

    def setArtistName(self) -> None:
        self.ui.artistname_label.setText(self.player.music_meta.artist)

    def clickedPauseBtn(self) -> None:
        self.player.pause()

    def clickedPlayBtn(self) -> None:
        self.audio_thread = self.createAudioThread()
        self.audio_thread.start()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.killPill.set()
        return super().closeEvent(a0)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    # main_window = uic.loadUi('pyplayer/interfaces/MainWindow.ui')
    # main_window.show()
    win = mywindow()
    win.show()
    app.exec()
    sys.exit(0)
