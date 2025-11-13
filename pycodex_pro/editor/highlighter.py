
import re
from PySide6 import QtGui

class BaseHL(QtGui.QSyntaxHighlighter):
    def __init__(self, doc):
        super().__init__(doc)
        self.rules = []  # list[(regex, QTextCharFormat)]

    def add_rule(self, pattern, fmt):
        self.rules.append((re.compile(pattern), fmt))

    def fmt(self, color=None, bold=False, italic=False):
        f = QtGui.QTextCharFormat()
        if color:
            f.setForeground(QtGui.QColor(*color))
        f.setFontWeight(QtGui.QFont.Bold if bold else QtGui.QFont.Normal)
        f.setFontItalic(italic)
        return f

    def highlightBlock(self, text):
        for rx, fmt in self.rules:
            for m in rx.finditer(text):
                start, end = m.span()
                self.setFormat(start, end - start, fmt)

class PythonHighlighter(BaseHL):
    def __init__(self, doc):
        super().__init__(doc)
        kw = r"\b(False|class|finally|is|return|None|continue|for|lambda|try|True|def|from|nonlocal|while|and|del|global|not|with|as|elif|if|or|yield|assert|else|import|pass|break|raise)\b"
        self.add_rule(kw, self.fmt((86,156,214), bold=True))
        self.add_rule(r"'[^'\\]*(?:\\.[^'\\]*)*'", self.fmt((206,145,120)))  # strings
        self.add_rule(r'"[^"\\]*(?:\\.[^"\\]*)*"', self.fmt((206,145,120)))
        self.add_rule(r"\b[0-9]+\b", self.fmt((181,206,168)))
        self.add_rule(r"#.*$", self.fmt((106,153,85)))

class JsonHighlighter(BaseHL):
    def __init__(self, doc):
        super().__init__(doc)
        self.add_rule(r'"[^"\\]*(?:\\.[^"\\]*)*"\s*:', self.fmt((156,220,254)))  # keys
        self.add_rule(r':\s*"[^"\\]*(?:\\.[^"\\]*)*"', self.fmt((206,145,120)))  # strings
        self.add_rule(r'\b(true|false|null)\b', self.fmt((86,156,214), bold=True))
        self.add_rule(r'\b[0-9]+\b', self.fmt((181,206,168)))

class MarkdownHighlighter(BaseHL):
    def __init__(self, doc):
        super().__init__(doc)
        self.add_rule(r'^#{1,6}\s.*$', self.fmt((86,156,214), bold=True))
        self.add_rule(r'`[^`]+`', self.fmt((181,206,168)))
        self.add_rule(r'\*\*[^\*]+\*\*', self.fmt((206,145,120)))
