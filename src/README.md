# PyCodeX Pro (VS Code–style editor in Python)

PyCodeX Pro is a compact, VS Code–style editor built with **PySide6**. It focuses on
look, responsiveness, and the core features most people expect from VS Code—without bloat.

### Highlights
- Tabbed editor with line numbers and current-line highlight
- Syntax highlighting (Python/JSON/Markdown basics)
- File explorer dock (fixed Windows path handling)
- Command palette with fuzzy filtering (Ctrl+Shift+P)
- Project-wide search (threaded)
- Integrated task runner (run arbitrary shell commands)
- Git panel (status, stage-all, commit) via `git` CLI
- Markdown preview dock
- Settings persisted to `~/.pycodex_pro/settings/settings.json`
- Tiny plugin system (drop `.py` into `.../plugins/user`)

> This is not affiliated with Microsoft or VS Code.

## Quick start
```bash
# 1) create & activate a virtualenv (optional but recommended)
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2) install dependencies
pip install -r requirements.txt

# 3) run
python run.py .            # open current folder as workspace
python run.py path\to\project
```

### Keys
- Ctrl+O: Open file dialog
- Ctrl+S: Save
- Ctrl+Shift+S: Save all
- Ctrl+W: Close tab
- Ctrl+F: Find in file
- Ctrl+Shift+F: Find in files
- Ctrl+Shift+P: Command palette
