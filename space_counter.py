#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from PyQt5 import QtGui, QtWidgets, QtCore


class SpaceRecorder(QtWidgets.QWidget):
    """ Counts how often the 'space' key is pressed and displays the count.

    Every time the 'space' key is pressed, a visual indicator is toggled, too.
    """

    def __init__(self):
        super().__init__()
        self.counter = 0
        self.initUI()

    def initUI(self):
        # set the text property of the widget we are inheriting
        self.text = "Please press 'space' repeatedly."
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('ClickRecorder')
        # widget should accept focus by click and tab key
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.show()

    def keyPressEvent(self, ev):
        if ev.key() == QtCore.Qt.Key_Space:
            self.counter += 1
            self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        self.drawRect(event, qp)
        qp.end()

    def drawText(self, event, qp):
        qp.setPen(QtGui.QColor(168, 34, 3))
        qp.setFont(QtGui.QFont('Decorative', 32))
        if self.counter > 0:
            self.text = str(self.counter)
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)

    def drawRect(self, event, qp):
        if (self.counter % 2) == 0:
            rect = QtCore.QRect(10, 10, 80, 80)
            qp.setBrush(QtGui.QColor(34, 34, 200))
        else:
            rect = QtCore.QRect(100, 10, 80, 80)
            qp.setBrush(QtGui.QColor(200, 34, 34))
        qp.drawRoundedRect(rect, 10.0, 10.0)


def main():
    app = QtWidgets.QApplication(sys.argv)
    # variable is never used, class automatically registers itself for Qt main loop:
    space = SpaceRecorder()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
