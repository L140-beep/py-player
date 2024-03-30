"""Main module."""

import sys
from threading import Thread, Event

from PyQt5.QtGui import QCloseEvent

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
        self.killThread = Event()
        self.player = AudioPlayer()

    def createAudioThread(self):
        return Thread(target=self.playAudio,
                      args=(self.killThread,))

    def playAudio(self, killPill: Event):
        self.killThread.clear()
        self.player.play('demos/Korol_i_SHut_-_Kukla_kolduna_62570545.mp3', killPill)

    def clickedPauseBtn(self):
        self.killThread.set()

    def clickedPlayBtn(self):
        self.audio_thread = self.createAudioThread()
        self.audio_thread.start()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.killThread.set()
        return super().closeEvent(a0)
    # TODO: убить тред


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    # main_window = uic.loadUi('pyplayer/interfaces/MainWindow.ui')
    # main_window.show()
    win = mywindow()
    win.show()
    app.exec()
    sys.exit(1)
