
import os
from PySide6 import QtWidgets, QtCore

class FileExplorerDock(QtWidgets.QDockWidget):
    open_file_requested = QtCore.Signal(str)

    def __init__(self, project_path: str, parent=None):
        super().__init__("Explorer", parent)
        self.setObjectName("FileExplorerDock")
        self.tree = QtWidgets.QTreeView(self)
        self.setWidget(self.tree)
        self.model = QtWidgets.QFileSystemModel(self.tree)
        self.model.setReadOnly(False)

        # Ensure str paths for Windows compatibility
        root = str(project_path)
        self.model.setRootPath(root)
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(root))

        self.tree.doubleClicked.connect(self._on_double_click)
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._menu)

    def _on_double_click(self, index):
        if self.model.isDir(index):
            return
        path = self.model.filePath(index)
        self.open_file_requested.emit(str(path))

    def _menu(self, pos):
        index = self.tree.indexAt(pos)
        menu = QtWidgets.QMenu(self)
        menu.addAction("New File", lambda: self._new_file(index))
        menu.addAction("New Folder", lambda: self._new_dir(index))
        if index.isValid():
            menu.addAction("Rename", lambda: self.tree.edit(index))
            menu.addAction("Delete", lambda: self._delete(index))
        menu.exec(self.tree.viewport().mapToGlobal(pos))

    def _base(self, index):
        return self.model.filePath(index) if index.isValid() else self.model.rootPath()

    def _new_file(self, index):
        base = self._base(index)
        name, ok = QtWidgets.QInputDialog.getText(self, "New file", "Filename:")
        if ok and name:
            open(os.path.join(base, name), "w", encoding="utf-8").close()

    def _new_dir(self, index):
        base = self._base(index)
        name, ok = QtWidgets.QInputDialog.getText(self, "New folder", "Name:")
        if ok and name:
            os.makedirs(os.path.join(base, name), exist_ok=True)

    def _delete(self, index):
        path = self.model.filePath(index)
        ret = QtWidgets.QMessageBox.question(self, "Delete", f"Delete {path}?")
        if ret == QtWidgets.QMessageBox.Yes:
            if self.model.isDir(index):
                import shutil; shutil.rmtree(path, ignore_errors=True)
            else:
                os.remove(path)
