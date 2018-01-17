import os
from click.testing import CliRunner
from escher_cli.escher import escher

TEST_PROJECT_ROOT = "../test_project"


def harness(*commands, wd=TEST_PROJECT_ROOT, ok=True, debug=True):
    """
    :param commands:
    :param wd: Set to None if the subcommand does not support work-directory
    :param ok: assert that the process runs without error.
    :return:
    """
    _c = ["--debug", *commands] if debug else commands
    _c = [*_c, "--work-directory", wd] if wd else _c
    print()
    print('════════════════════ SCRIPT ════════════════════')
    print(f"escher {' '.join(_c)}")
    print('────────────────────────────────────────────────')
    runner = CliRunner()
    result = runner.invoke(escher, _c)
    if ok:
        assert result.exit_code == 0, result.output
    else:
        assert result.exit_code != 0, result.output
    return result


def test():
    result = harness(debug=False, wd=None)
    print(result.output)


def test_run_help():
    result = harness('run', '-h')
    print(result.output)


def test_run():
    """should run the default script"""
    result = harness('run', ok=True)
    print(result.output)


def test_run_rc():
    """should run the default script"""
    result = harness('run', 'test', ok=True)
    print(result.output)


def test_run_external():
    """should run the default script"""
    result = harness('run', 'scripts/test.escher', ok=True)
    print(result.output)
