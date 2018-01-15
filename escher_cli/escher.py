#!python
"""Example script
escher.py-cli --config-file="experiment.yaml" --starting-index=0 --extra-arguments-etc
"""
from os import getcwd
from pprint import pformat
import click
from click import Abort
from escher_cli import helpers
import escher_cli.helpers
from escher_cli.local_runner import main
from subprocess import check_call


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--debug', is_flag=True)
def escher(debug):
    """Escher-cli is a command line tool for your ML training."""
    if debug:  # set debug flag in helpers
        escher_cli.helpers.set_debug()
    escher_cli.helpers.debug("debug mode is ON.")


@escher.command(context_settings=dict(ignore_unknown_options=True))
def init():
    """initialize the project with an .escher runcom file, similar to `.babelrc` or `.bashrc`"""
    pass


ESCHERRC_PATH = ".escher"


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
        ✗ escher run test  # runs the test script defined in .escher
        ✗ escher run scripts/test.escher
        ✗ escher run scripts/test.escher -w gpu-worker
        ✗ escher run scripts/test.escher -w gpu-worker -b
    """
    escher_cli.helpers.debug("locals:\n", pformat(locals()))
    try:
        config_rc = helpers.load_config(ESCHERRC_PATH)
    except FileNotFoundError as e:
        click.echo(f"trying to read `{ESCHERRC_PATH}` but \n{e}")
        raise Abort(e)
    escher_cli.helpers.debug("config_rc:\n", pformat(vars(config_rc)))

    if config_rc.scripts:
        escher_cli.helpers.debug(config_rc.scripts)
    if config_rc.scripts and script in config_rc.scripts:
        _s = config_rc.scripts[script].strip()
        escher_cli.helpers.debug('is existing script', _s)
        # todo: need to take care of remote execution
        # todo: need to make sure environment is set correctly for this run.
        # todo: is this blocking?
        # todo: run *.escher file directly as escher script without bash. Parse as ^(\b*)[\.\\\/A-z]\.escher\b(.*)
        return check_call(" ".join([_s, *args]), shell=True)
    else:
        escher_cli.helpers.debug('looking for script', script)
        _s = script

    if worker == "local":
        # todo: move logic in `main` here?
        main(_s)
    else:
        # todo: imeplement other type of workers.
        # todo: aws worker, require remote daemon and ws graphQL server
        pass
        
