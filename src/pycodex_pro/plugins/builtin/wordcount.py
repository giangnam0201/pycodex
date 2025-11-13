
def activate(api):
    def run():
        ed = api.main_window.editor.current_editor()
        if not ed: return
        text = ed.toPlainText()
        words = len(text.split())
        chars = len(text)
        api.main_window.statusBar().showMessage(f"Words: {words} | Chars: {chars}")
    api.register_command("plugin.wordcount", "Word Count (active tab)", run)
