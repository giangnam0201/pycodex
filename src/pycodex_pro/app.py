
import os, sys, pathlib
from PySide6 import QtWidgets, QtGui
from .main_window import MainWindow
from .utils.paths import ensure_app_dirs, resolve_project_path
from .utils.theme import apply_dark_palette

def main(argv=None):
    argv = sys.argv if argv is None else argv
    app = QtWidgets.QApplication(argv)
    app.setOrganizationName("PyCodeXPro")
    app.setApplicationName("PyCodeX Pro")
    QtWidgets.QApplication.setApplicationDisplayName("PyCodeX Pro")

    # Looks
    app.setStyle("Fusion")
    apply_dark_palette(app)

    ensure_app_dirs()
    project_arg = argv[1] if len(argv) > 1 else os.getcwd()
    project_path = resolve_project_path(project_arg)

    win = MainWindow(project_path=project_path)
    win.show()
    return app.exec()
