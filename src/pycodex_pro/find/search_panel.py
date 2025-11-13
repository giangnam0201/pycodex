
import os, re, threading, queue, pathlib
from PySide6 import QtWidgets, QtCore

class Worker(QtCore.QObject):
    result = QtCore.Signal(str, int, str)
    finished = QtCore.Signal()

    def __init__(self, root: str, pattern: str, regex: bool, case: bool, whole: bool):
        super().__init__()
        self.root = root
        self.pattern = pattern
        self.regex = regex
        self.case = case
        self.whole = whole
        self._stop = False

    @QtCore.Slot()
    def run(self):
        pat = self.pattern
        flags = 0 if self.case else re.IGNORECASE
        rx = re.compile(pat, flags) if self.regex else None
        for r, _, files in os.walk(self.root):
            for f in files:
                p = os.path.join(r, f)
                try:
                    with open(p, "r", encoding="utf-8", errors="ignore") as fh:
                        for i, line in enumerate(fh, 1):
                            s = line.rstrip("\n")
                            if rx:
                                m = rx.search(s)
                                if m:
                                    self.result.emit(p, i, s.strip())
                            else:
                                hay = s if self.case else s.lower()
                                needle = pat if self.case else pat.lower()
                                if self.whole:
                                    if any(tok == needle for tok in re.findall(r"\w+", hay)):
                                        self.result.emit(p, i, s.strip())
                                else:
                                    if needle in hay:
                                        self.result.emit(p, i, s.strip())
                except Exception:
                    pass
        self.finished.emit()

class SearchDock(QtWidgets.QDockWidget):
    def __init__(self, project_path: str, editor, parent=None):
        super().__init__("Search", parent)
        self.setObjectName("SearchDock")
        self.editor = editor
        w = QtWidgets.QWidget(self)
        self.setWidget(w)
        lay = QtWidgets.QVBoxLayout(w)
        form = QtWidgets.QHBoxLayout()
        self.pattern = QtWidgets.QLineEdit()
        self.regex = QtWidgets.QCheckBox("Regex")
        self.case = QtWidgets.QCheckBox("Case")
        self.whole = QtWidgets.QCheckBox("Whole word")
        self.btn = QtWidgets.QPushButton("Search")
        self.btn.clicked.connect(self._start)
        for x in (self.pattern, self.regex, self.case, self.whole, self.btn):
            form.addWidget(x)
        lay.addLayout(form)
        self.list = QtWidgets.QListWidget()
        self.list.itemActivated.connect(self._open)
        lay.addWidget(self.list)
        self.root = project_path
        self._thread = None
        self._worker = None

    def show_and_focus(self):
        self.show(); self.raise_(); self.activateWindow()
        self.pattern.setFocus()

    def _start(self):
        self.list.clear()
        pat = self.pattern.text().strip()
        if not pat: return
        self._thread = QtCore.QThread()
        self._worker = Worker(self.root, pat, self.regex.isChecked(), self.case.isChecked(), self.whole.isChecked())
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.result.connect(self._add)
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.start()

    def _add(self, path, line_no, text):
        it = QtWidgets.QListWidgetItem(f"{path}:{line_no} — {text[:120]}")
        it.setData(QtCore.Qt.UserRole, (path, int(line_no)))
        self.list.addItem(it)

    def _open(self, item):
        path, line = item.data(QtCore.Qt.UserRole)
        self.parent().editor.open_path(path)
