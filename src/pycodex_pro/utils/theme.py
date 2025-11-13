
from PySide6 import QtGui, QtWidgets

def apply_dark_palette(app: QtWidgets.QApplication):
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(40, 40, 45))
    palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(220, 220, 220))
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(30, 30, 33))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(40, 40, 45))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(220, 220, 220))
    palette.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(220, 220, 220))
    palette.setColor(QtGui.QPalette.Text, QtGui.QColor(220, 220, 220))
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(45, 45, 50))
    palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(220, 220, 220))
    palette.setColor(QtGui.QPalette.BrightText, QtGui.QColor(255, 0, 0))
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(64, 128, 255))
    palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(0, 0, 0))
    app.setPalette(palette)
