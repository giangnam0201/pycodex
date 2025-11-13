
import importlib.util, pathlib, traceback
from ..utils.paths import user_config_dir
from .api import PluginAPI

class PluginManager:
    def __init__(self, main_window, registry):
        self.win = main_window
        self.registry = registry
        self.api = PluginAPI(main_window, registry)
        self._loaded = {}

    def load_builtin_plugins(self):
        base = pathlib.Path(__file__).parent / "builtin"
        self._load_dir(base)

    def load_user_plugins(self):
        base = user_config_dir() / "plugins" / "user"
        self._load_dir(base)

    def reload_all(self):
        self._loaded.clear()
        self.load_builtin_plugins()
        self.load_user_plugins()

    def _load_dir(self, directory: pathlib.Path):
        directory.mkdir(parents=True, exist_ok=True)
        for py in directory.glob("*.py"):
            self._load(py)

    def _load(self, path: pathlib.Path):
        name = path.stem
        spec = importlib.util.spec_from_file_location(f"pycodex_plugin_{name}", path)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)  # type: ignore
            if hasattr(mod, "activate"):
                mod.activate(self.api)
            self._loaded[name] = mod
        except Exception as e:
            print("Failed to load plugin", path, e)
            traceback.print_exc()
