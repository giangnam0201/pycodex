
import pathlib, os

def user_config_dir() -> pathlib.Path:
    return pathlib.Path.home() / ".pycodex_pro"

def ensure_app_dirs():
    base = user_config_dir()
    (base / "plugins" / "user").mkdir(parents=True, exist_ok=True)
    (base / "settings").mkdir(parents=True, exist_ok=True)
    (base / "logs").mkdir(parents=True, exist_ok=True)

def resolve_project_path(path_like) -> str:
    # Always return a string for Qt API compatibility on Windows.
    p = pathlib.Path(path_like).expanduser().resolve()
    if p.exists():
        return str(p)
    return str(pathlib.Path.cwd())
