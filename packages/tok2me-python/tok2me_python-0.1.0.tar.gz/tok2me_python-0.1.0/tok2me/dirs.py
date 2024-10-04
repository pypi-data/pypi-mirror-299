import os
from pathlib import Path

from platformdirs import user_config_dir, user_data_dir


def get_config_dir() -> Path:
    return Path(user_config_dir("tok2me"))


def get_readline_history_file() -> Path:
    # TODO: move to data dir
    return get_config_dir() / "history"


def get_data_dir() -> Path:
    # used in testing, so must take precedence
    if "XDG_DATA_HOME" in os.environ:
        return Path(os.environ["XDG_DATA_HOME"]) / "tok2me"

    # just a workaround for me personally
    old = Path("~/.local/share/tok2me").expanduser()
    if old.exists():
        return old

    return Path(user_data_dir("tok2me"))


def get_logs_dir() -> Path:
    """Get the path for **conversation logs** (not to be confused with the logger file)"""
    path = get_data_dir() / "logs"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _init_paths():
    # create all paths
    for path in [get_config_dir(), get_data_dir(), get_logs_dir()]:
        path.mkdir(parents=True, exist_ok=True)


# run once on init
_init_paths()
