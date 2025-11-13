
import subprocess, os
from PySide6 import QtWidgets, QtCore

def git_run(args, cwd):
    try:
        out = subprocess.check_output(["git"] + args, cwd=cwd, text=True, stderr=subprocess.STDOUT)
        return out
    except Exception as e:
        return str(e)

class GitDock(QtWidgets.QDockWidget):
    def __init__(self, project_path: str, parent=None):
        super().__init__("Git", parent)
        self.setObjectName("GitDock")
        self.root = project_path
        w = QtWidgets.QWidget(self); self.setWidget(w)
        v = QtWidgets.QVBoxLayout(w)
        h = QtWidgets.QHBoxLayout()
        self.msg = QtWidgets.QLineEdit(); self.msg.setPlaceholderText("Commit message")
        self.stage_btn = QtWidgets.QPushButton("Stage All")
        self.commit_btn = QtWidgets.QPushButton("Commit")
        self.refresh_btn = QtWidgets.QPushButton("Refresh")
        self.stage_btn.clicked.connect(self._stage_all)
        self.commit_btn.clicked.connect(self._commit)
        self.refresh_btn.clicked.connect(self.refresh)
        for x in (self.msg, self.stage_btn, self.commit_btn, self.refresh_btn):
            h.addWidget(x)
        v.addLayout(h)
        self.out = QtWidgets.QPlainTextEdit(); self.out.setReadOnly(True)
        v.addWidget(self.out)
        self.refresh()

    def refresh(self):
        self.out.setPlainText(git_run(["status"], self.root))

    def _stage_all(self):
        self.out.appendPlainText(git_run(["add", "-A"], self.root))
        self.refresh()

    def _commit(self):
        msg = self.msg.text().strip() or "update"
        self.out.appendPlainText(git_run(["commit", "-m", msg], self.root))
        self.refresh()
