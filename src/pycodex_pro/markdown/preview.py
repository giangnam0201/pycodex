
from PySide6 import QtWidgets
import markdown

class MarkdownPreviewDock(QtWidgets.QDockWidget):
    def __init__(self, editor_area, parent=None):
        super().__init__("Markdown Preview", parent)
        self.setObjectName("MarkdownPreviewDock")
        self.editor_area = editor_area
        w = QtWidgets.QTextBrowser(self)
        self.setWidget(w)
        self.editor_area.currentChanged.connect(self._refresh)

    def _refresh(self, idx):
        ed = self.editor_area.current_editor()
        if not ed:
            self.widget().clear(); return
        path = ed.path or ""
        if not path.lower().endswith(".md"):
            self.widget().setHtml("<i>Open a .md file to preview.</i>"); return
        html = markdown.markdown(ed.toPlainText(), extensions=["fenced_code"])
        self.widget().setHtml(html)
