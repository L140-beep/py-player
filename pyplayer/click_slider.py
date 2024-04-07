from typing import Any, Callable, List

from PyQt5 import QtWidgets


from PyQt5.QtGui import QMouseEvent


class ClickSlider(QtWidgets.QSlider):
    """Слайдер, поддерживающий реакцию на клики."""

    def __init__(self, parent: QtWidgets.QWidget | None,
                 func: Callable,
                 args: List[Any]):
        self.func = func
        self.args = args
        super().__init__(parent)

    def mouseReleaseEvent(self, ev: QMouseEvent | None) -> None:
        self.func(self, ev, *self.args)
        return super().mouseReleaseEvent(ev)
