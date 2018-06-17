from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPainter, QPen, QColor
from pack import Pack


class UI(QMainWindow):
    def __init__(self, pack: Pack):
        super().__init__()

        self._pack = pack
        self.resize(pack.w, pack.h)
        self.setFixedSize(pack.w, pack.h)
        self._painter = QPainter()

    def paintEvent(self, qpe):
        self._painter.begin(self)
        self._painter.setBrush(Qt.SolidPattern)

        for rect in self._pack.used_rectangles:
            self._painter.drawRect(rect.x, rect.y, rect.w, rect.h)

        self._painter.end()
