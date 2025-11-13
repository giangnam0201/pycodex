
import subprocess, os
from PySide6 import QtWidgets, QtCore

class TaskRunnerDock(QtWidgets.QDockWidget):
    def __init__(self, project_path: str, parent=None):
        super().__init__("Tasks", parent)
        self.setObjectName("TaskRunnerDock")
        self.project_path = project_path
        w = QtWidgets.QWidget(self); self.setWidget(w)
        v = QtWidgets.QVBoxLayout(w)
        h = QtWidgets.QHBoxLayout()
        self.cmd = QtWidgets.QLineEdit("python --version")
        self.run_btn = QtWidgets.QPushButton("Run")
        self.run_btn.clicked.connect(self._run)
        h.addWidget(self.cmd); h.addWidget(self.run_btn)
        v.addLayout(h)
        self.out = QtWidgets.QPlainTextEdit(); self.out.setReadOnly(True)
        v.addWidget(self.out)

    def show_and_focus(self):
        self.show(); self.raise_(); self.activateWindow(); self.cmd.setFocus()

    def _run(self):
        cmd = self.cmd.text().strip()
        if not cmd: return
        self.out.appendPlainText(f"$ {cmd}\n")
        QtCore.QTimer.singleShot(0, lambda: self._exec(cmd))

    def _exec(self, cmd):
        try:
            proc = subprocess.Popen(cmd, cwd=self.project_path, shell=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    text=True, bufsize=1, universal_newlines=True)
            for line in proc.stdout:
                self.out.appendPlainText(line.rstrip())
            proc.wait()
            self.out.appendPlainText(f"\n[exit {proc.returncode}]")
        except Exception as e:
            self.out.appendPlainText(str(e))
