#!python
"""Example script
escher.py-cli --config-file="experiment.yaml" --starting-index=0 --extra-arguments-etc
"""
from functools import reduce
from os import getcwd, environ
from pprint import pformat
import click
import re

from click import Abort
import escher_cli
from escher_cli import helpers, runner
from subprocess import check_call


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--debug', is_flag=True)
def escher(debug):
    """Escher-cli is a command line tool for your ML training."""
    if debug:  # set debug flag in helpers
        helpers.set_debug()
    helpers.debug("debug mode is ON.")


@escher.command(context_settings=dict(ignore_unknown_options=True))
def init():
    """initialize the project with an .escher runcom file, similar to `.babelrc` or `.bashrc`"""
    pass


@escher.command(context_settings=dict(ignore_unknown_options=True))
@click.pass_context
# @escher.py.argument()
@click.option('--worker', '-w', default='local', type=str)
@click.argument('script', default="default", type=str)
@click.argument('--work-directory', default=getcwd(), type=str)
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def run(ctx, worker, script, work_directory, args):
    return runner.run(worker, script, work_directory, args)
