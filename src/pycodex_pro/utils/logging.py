
import logging, pathlib, datetime

_LOGGER = None

def get_logger(name="pycodex_pro"):
    global _LOGGER
    if _LOGGER is not None:
        return _LOGGER.getChild(name) if name != "pycodex_pro" else _LOGGER
    logdir = pathlib.Path.home() / ".pycodex_pro" / "logs"
    logdir.mkdir(parents=True, exist_ok=True)
    logfile = logdir / f"app-{datetime.date.today().isoformat()}.log"
    logger = logging.getLogger("pycodex_pro")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(logfile, encoding="utf-8")
    sh = logging.StreamHandler()
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    fh.setFormatter(fmt); sh.setFormatter(fmt)
    logger.addHandler(fh); logger.addHandler(sh)
    _LOGGER = logger
    return logger if name == "pycodex_pro" else logger.getChild(name)
