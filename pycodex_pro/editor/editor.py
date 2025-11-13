
import os, pathlib, re
from PySide6 import QtWidgets, QtCore, QtGui
from .line_numbers import LineNumberArea
from .highlighter import PythonHighlighter, JsonHighlighter, MarkdownHighlighter

class EditorArea(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_index)

    # ---- actions ----
    def open_file_dialog(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open file", os.getcwd())
        if path:
            self.open_path(path)

    def open_path(self, path: str):
        path = str(path)
        for i in range(self.count()):
            w = self.widget(i)
            if isinstance(w, CodeEditor) and w.path == path:
                self.setCurrentIndex(i)
                return
        ed = CodeEditor(path)
        name = os.path.basename(path) if path else "untitled"
        self.addTab(ed, name)
        self.setCurrentWidget(ed)

    def current_editor(self):
        w = self.currentWidget()
        return w if isinstance(w, CodeEditor) else None

    def save_current(self):
        ed = self.current_editor()
        if ed: ed.save()

    def save_all(self):
        for i in range(self.count()):
            w = self.widget(i)
            if isinstance(w, CodeEditor):
                w.save()

    def close_current(self):
        i = self.currentIndex()
        if i >= 0:
            self.close_index(i)

    def close_index(self, idx):
        w = self.widget(idx)
        if isinstance(w, CodeEditor) and w.maybe_save_changes():
            self.removeTab(idx)
            w.deleteLater()

    def find_in_current(self):
        ed = self.current_editor()
        if not ed: return
        ed.show_find()

class CodeEditor(QtWidgets.QPlainTextEdit):
    def __init__(self, path=None, parent=None):
        super().__init__(parent)
        self.path = path
        self.setTabStopDistance(4 * self.fontMetrics().horizontalAdvance(' '))
        self.document().setDefaultFont(QtGui.QFont("Consolas", 10))

        # Line number area
        self.line_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_area_width)
        self.updateRequest.connect(self.update_line_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        # Highlighter
        self.highlighter = None
        self._apply_highlighter()

        # State
        self._dirty = False
        self.textChanged.connect(self._on_text_changed)

        # Load content
        if self.path and os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8", errors="ignore") as f:
                self.setPlainText(f.read())
            self._dirty = False

    # ---- highlighter ----
    def _apply_highlighter(self):
        lexer = (os.path.splitext(self.path or "")[1]).lower()
        if lexer == ".json":
            self.highlighter = JsonHighlighter(self.document())
        elif lexer == ".md" or lexer == ".markdown":
            self.highlighter = MarkdownHighlighter(self.document())
        else:
            self.highlighter = PythonHighlighter(self.document())

    # ---- line numbers ----
    def line_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        return 12 + self.fontMetrics().horizontalAdvance('9') * digits

    def update_line_area_width(self, *args):
        self.setViewportMargins(self.line_area_width(), 0, 0, 0)

    def update_line_area(self, rect, dy):
        if dy:
            self.line_area.scroll(0, dy)
        else:
            self.line_area.update(0, rect.y(), self.line_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_area_width()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        cr = self.contentsRect()
        self.line_area.setGeometry(QtCore.QRect(cr.left(), cr.top(), self.line_area_width(), cr.height()))

    def highlight_current_line(self):
        sel = QtWidgets.QTextEdit.ExtraSelection()
        sel.format.setBackground(QtGui.QColor(50, 50, 60))
        sel.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
        sel.cursor = self.textCursor()
        sel.cursor.clearSelection()
        self.setExtraSelections([sel])

    def paintEvent(self, event):
        super().paintEvent(event)

    # ---- file ops ----
    def maybe_save_changes(self):
        if not self._dirty:
            return True
        ret = QtWidgets.QMessageBox.question(self, "Save changes?",
            f"Save changes to {self.path or 'untitled'} before closing?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
        if ret == QtWidgets.QMessageBox.Cancel:
            return False
        if ret == QtWidgets.QMessageBox.Yes:
            self.save()
        return True

    def save(self):
        if not self.path:
            path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save file", os.getcwd())
            if not path: return
            self.path = path
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(self.toPlainText())
        self._dirty = False

    # ---- find ----
    def show_find(self):
        text, ok = QtWidgets.QInputDialog.getText(self, "Find", "Text:")
        if ok and text:
            self._find_text(text)

    def _find_text(self, text):
        if not self.find(text):
            cursor = self.textCursor()
            cursor.movePosition(QtGui.QTextCursor.Start)
            self.setTextCursor(cursor)
            self.find(text)

    # ---- internals ----
    def _on_text_changed(self):
        self._dirty = True
