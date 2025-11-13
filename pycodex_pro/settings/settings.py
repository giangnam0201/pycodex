
import json, pathlib
from ..utils.paths import user_config_dir

class Settings:
    def __init__(self):
        self.path = user_config_dir() / "settings" / "settings.json"
        self.data = {"theme": "dark", "tab_width": 4}
        self.load()

    def load(self):
        try:
            if self.path.exists():
                self.data.update(json.loads(self.path.read_text(encoding="utf-8")))
        except Exception:
            pass

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2), encoding="utf-8")
