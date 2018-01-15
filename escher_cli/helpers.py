from os import getcwd
from pathlib import Path

from ruamel.yaml import YAML

# I hate doing this.
from waterbear import DefaultBear

DEBUG = False


def set_debug():
    global DEBUG
    DEBUG = True


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def load_config(config_file_path):
    yaml = YAML(typ='unsafe', pure=True)
    p = Path(config_file_path)
    parsed = yaml.load_all(Path(config_file_path))
    data = next(parsed)
    return DefaultBear(None, **data)
