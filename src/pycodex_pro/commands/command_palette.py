
from PySide6 import QtWidgets, QtCore

def score(query: str, text: str) -> int:
    # Very small fuzzy score (subsequence match + density)
    q = query.lower()
    t = text.lower()
    pos = -1; hits = 0
    for ch in q:
        pos = t.find(ch, pos + 1)
        if pos == -1: return -1
        hits += 1
    return hits * 100 - (pos - len(q))  # crude density bias

class CommandPalette(QtWidgets.QDialog):
    def __init__(self, registry, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Command Palette")
        self.resize(640, 440)
        self.registry = registry
        layout = QtWidgets.QVBoxLayout(self)
        self.edit = QtWidgets.QLineEdit(self); self.edit.setPlaceholderText("Type a command...")
        self.list = QtWidgets.QListWidget(self)
        layout.addWidget(self.edit); layout.addWidget(self.list)
        for cid, label in self.registry.list():
            it = QtWidgets.QListWidgetItem(f"{label} ({cid})")
            it.setData(QtCore.Qt.UserRole, cid)
            self.list.addItem(it)
        self.edit.textChanged.connect(self._filter)
        self.list.itemActivated.connect(self._run)

    def _filter(self, text):
        if not text:
            for i in range(self.list.count()):
                self.list.item(i).setHidden(False)
            return
        scores = []
        for i in range(self.list.count()):
            it = self.list.item(i)
            s = score(text, it.text())
            it.setHidden(s < 0)
            if s >= 0:
                scores.append((s, it.text(), it))
        # sort by score
        for idx, (_, _, it) in enumerate(sorted(scores, key=lambda x: (-x[0], x[1]))):
            self.list.takeItem(self.list.row(it))
            self.list.insertItem(idx, it)

    def _run(self, item):
        cid = item.data(QtCore.Qt.UserRole)
        self.registry.run(cid)
        self.accept()
