from os import getcwd
from pathlib import Path

import re

import click
from _ruamel_yaml import ScannerError
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
    """should raise ScannerError if there is a problem in the yaml file."""
    yaml = YAML(typ='unsafe', pure=True)
    p = Path(config_file_path)
    parsed = yaml.load_all(p)
    data = next(parsed)
    return DefaultBear(None, **data)


def is_str(s):
    return type(s) is str


def is_list_tuple_set(s):
    return type(s) in (list, tuple, set)


ESCHER_SCRIPT_REGEX = re.compile('^(\s*)([./\\\\A-z]*)\.escher(.*)$')


def is_script(s):
    return is_str(s) and ESCHER_SCRIPT_REGEX.match(s)
