#!python
"""Example script
escherd  # reads in the .escher file
"""
from functools import reduce
from os import getcwd, environ
from pprint import pformat
import click
import re

from click import Abort
from escher_cli import helpers
from escher_cli import local_runner
from subprocess import check_call


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--debug', is_flag=True)
def escherd(debug):
    """the daemon for the escher-cli"""
    if debug:  # set debug flag in helpers
        helpers.set_debug()
    helpers.debug("debug mode is ON.")


@escherd.command(context_settings=dict(ignore_unknown_options=True))
def init():
    """initialize the project with an .escher runcom file, similar to `.babelrc` or `.bashrc`"""
    pass



@escher.command(context_settings=dict(ignore_unknown_options=True))
@click.pass_context
# @escher.py.argument()
@click.option('--worker', '-w', default='local', type=str)
@click.argument('script', default="default", type=str)
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def run(ctx, worker, script, args):
    """
    execute a script defined in .escher, or via a configuration file path.

    Two config file types are supported: escher script, or bash script.

    \b
    Examples:
        ✓ escher run -h/--help
        ✓ escher run  # runs the default script
        ✓ escher run test  # runs the test script defined in .escher
        ✓ escher run scripts/test.escher
        # Need worker daemon
        ✗ escher run scripts/test.escher -w gpu-worker
        ✗ escher run scripts/test.escher -w gpu-worker -b
    """
    helpers.debug("locals:\n", pformat(locals()))
    try:
        config_rc = helpers.load_config(ESCHERRC_PATH)
    except FileNotFoundError as e:
        click.echo(f"trying to read `{ESCHERRC_PATH}` but \n{e}")
        raise Abort(e)
    helpers.debug("config_rc:\n", pformat(vars(config_rc)))

    if config_rc.scripts:
        helpers.debug(config_rc.scripts)
    if config_rc.scripts and script in config_rc.scripts:
        shell, _s = True, config_rc.scripts[script].strip()
        helpers.debug(f'run script from `.escher` runcom file: "{_s}"')
        # done: run *.escher file directly as escher script without bash. Parse as ^(\b*)[\.\\\/A-z]\.escher\b(.*)
    else:
        # todo: need to make sure environment is set correctly for this run.
        # todo: set environment variables
        helpers.debug('looking for script', script)
        shell, _s = False, [script, *args]

    if worker == "local":
        # todo: need to take care of remote execution
        # todo: need to make sure environment is set correctly for this run.
        # todo: is this blocking?
        # todo pass-through extra arguments
        # todo: move logic in `main` here?
        if helpers.is_script(_s):
            local_runner.main(_s)
        elif helpers.is_list_tuple_set(_s) and _s and helpers.is_script(_s[0]):
            local_runner.main(" ".join(_s))
        else:
            helpers.debug(_s, shell)
            my_env = environ.copy()
            return check_call(_s, shell=shell, env=my_env)
    else:
        # todo: implement other type of workers.
        # todo: aws worker, require remote daemon and ws graphQL server
        pass
