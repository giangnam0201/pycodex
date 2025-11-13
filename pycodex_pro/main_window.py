
import os, pathlib, subprocess
from PySide6 import QtWidgets, QtCore, QtGui

from .editor.editor import EditorArea
from .explorer.file_explorer import FileExplorerDock
from .find.search_panel import SearchDock
from .commands.registry import CommandRegistry
from .commands.command_palette import CommandPalette
from .terminal.runner import TaskRunnerDock
from .git.git_panel import GitDock
from .markdown.preview import MarkdownPreviewDock
from .plugins.manager import PluginManager
from .utils.logging import get_logger

log = get_logger(__name__)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, project_path: str):
        super().__init__()
        self.setWindowTitle("PyCodeX Pro")
        self.resize(1280, 840)
        self.project_path = project_path  # keep as str

        # Central editor
        self.editor = EditorArea(self)
        self.setCentralWidget(self.editor)

        # Docks
        self.explorer = FileExplorerDock(self.project_path, self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.explorer)

        self.search = SearchDock(self.project_path, self.editor, self)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.search)

        self.tasks = TaskRunnerDock(self.project_path, self)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.tasks)

        self.git = GitDock(self.project_path, self)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.git)

        self.md = MarkdownPreviewDock(self.editor, self)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.md)

        # Commands & plugins
        self.commands = CommandRegistry(self)
        self._register_core_commands()
        self.plugins = PluginManager(self, self.commands)
        self.plugins.load_builtin_plugins()
        self.plugins.load_user_plugins()

        # Menus / toolbar
        self._init_menu()
        self._init_toolbar()

        # Connections
        self.explorer.open_file_requested.connect(self.editor.open_path)

    # ----- UI -----
    def _init_menu(self):
        mb = self.menuBar()

        file_menu = mb.addMenu("&File")
        file_menu.addAction("Open File...", self.editor.open_file_dialog, "Ctrl+O")
        file_menu.addAction("Save", self.editor.save_current, "Ctrl+S")
        file_menu.addAction("Save All", self.editor.save_all, "Ctrl+Shift+S")
        file_menu.addAction("Close Tab", self.editor.close_current, "Ctrl+W")
        file_menu.addSeparator()
        file_menu.addAction("Quit", self.close)

        edit_menu = mb.addMenu("&Edit")
        edit_menu.addAction("Find", self.editor.find_in_current, "Ctrl+F")
        edit_menu.addAction("Find in Files", self.search.show_and_focus, "Ctrl+Shift+F")

        view_menu = mb.addMenu("&View")
        view_menu.addAction("Command Palette", self.show_command_palette, "Ctrl+Shift+P")
        view_menu.addAction("Toggle Markdown Preview", self._toggle_md)

        tools_menu = mb.addMenu("&Tools")
        tools_menu.addAction("Run Task...", self.tasks.show_and_focus)
        tools_menu.addAction("Reload Plugins", self.plugins.reload_all)

        git_menu = mb.addMenu("&Git")
        git_menu.addAction("Refresh", self.git.refresh)

        help_menu = mb.addMenu("&Help")
        help_menu.addAction("About", self._about)

    def _init_toolbar(self):
        tb = self.addToolBar("Main")
        tb.addAction("Open", self.editor.open_file_dialog)
        tb.addAction("Save", self.editor.save_current)
        tb.addAction("Search", self.search.show_and_focus)

    # ----- Commands -----
    def _register_core_commands(self):
        self.commands.register("app.about", "About", self._about)
        self.commands.register("editor.openFile", "Open File...", self.editor.open_file_dialog)
        self.commands.register("editor.save", "Save", self.editor.save_current)
        self.commands.register("editor.saveAll", "Save All", self.editor.save_all)
        self.commands.register("search.project", "Find in Files", self.search.show_and_focus)
        self.commands.register("tasks.run", "Run Task...", self.tasks.show_and_focus)
        self.commands.register("markdown.toggle", "Toggle Markdown Preview", self._toggle_md)

    # ----- Actions -----
    def _about(self):
        QtWidgets.QMessageBox.information(self, "About PyCodeX Pro",
            "PyCodeX Pro\nA compact, VS Code–style editor built with PySide6.\n"
            "Not affiliated with Microsoft/VS Code.")

    def show_command_palette(self):
        dlg = CommandPalette(self.commands, self)
        dlg.exec()

    def _toggle_md(self):
        self.md.setVisible(not self.md.isVisible())
