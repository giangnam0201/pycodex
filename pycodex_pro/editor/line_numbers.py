
from PySide6 import QtWidgets, QtCore, QtGui

class LineNumberArea(QtWidgets.QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QtCore.QSize(self.editor.line_area_width(), 0)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(event.rect(), QtGui.QColor(32, 32, 36))

        block = self.editor.firstVisibleBlock()
        block_num = block.blockNumber()
        top = int(self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top())
        bottom = top + int(self.editor.blockBoundingRect(block).height())
        fm = self.editor.fontMetrics()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_num + 1)
                painter.setPen(QtGui.QColor(120, 120, 130))
                painter.drawText(0, top, self.width() - 6, fm.height(), QtCore.Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + int(self.editor.blockBoundingRect(block).height())
            block_num += 1
