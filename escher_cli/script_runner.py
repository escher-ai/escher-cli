"""escher_cli.run module, all of the run logic for the escher_cli."""
from os import environ, getcwd, chdir
from pprint import pformat
from subprocess import check_call

import click
from _ruamel_yaml import ScannerError
from click import Abort
from escher_cli import helpers, escher_runner

ESCHERRC_PATH = ".escher"


def run(worker, script, work_directory, args):
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
    if work_directory:
        chdir(work_directory)

    helpers.debug("locals:\n", pformat(locals()))
    try:
        config_rc = helpers.load_config(ESCHERRC_PATH)
    except FileNotFoundError as e:
        click.echo(f"trying to read `{ESCHERRC_PATH}` but \n{e}")
        raise Abort(e)
    except ScannerError as e:
        click.echo(f"A ScannerError has occurred when parsing the yaml configuration file "
                   f"\n\t{ESCHERRC_PATH}"
                   f"\nunder work directory"
                   f"\n\t{getcwd()}"
                   f"\nPlease check according to the error message:"
                   f"\n{e}")
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
            escher_runner.main(_s)
        elif helpers.is_list_tuple_set(_s) and _s and helpers.is_script(_s[0]):
            escher_runner.main(" ".join(_s))
        else:
            helpers.debug(_s, shell)
            my_env = environ.copy()
            return check_call(_s, shell=shell, env=my_env)
    else:
        # todo: implement other type of workers.
        # todo: aws worker, require remote daemon and ws graphQL server
        pass
