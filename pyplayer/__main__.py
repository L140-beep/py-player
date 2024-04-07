"""Main module."""

import sys

from PyQt5 import QtWidgets
from pyplayer.player_controller import Player

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = Player()
    win.show()
    app.exec()
    sys.exit(0)
