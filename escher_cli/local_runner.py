import logging
from copy import deepcopy
from os import getcwd
from pathlib import Path
from subprocess import check_call

from escher import RunTimeParams, hydrate_templates
# noinspection PyUnresolvedReferences
from escher_cli.helpers import load_config
from params_proto import is_hidden, cli_parse, Proto, ParamsProto
from pathos.multiprocessing import ProcessingPool
from ruamel.yaml import YAML, sys, os
from waterbear import DefaultBear, Bear


class RunnerConfig:
    """configuration for the runner <<= see schema."""
    max_concurrent = 4  # type: int


class RunConfig(Bear):
    """config namespare for the run script"""
    config = DefaultBear(None)  # type: RunnerConfig
    env = {}  # type: dict
    run = 'python main.py {args}'  # type: str
    default_args = {}  # type: dict
    args = {}  # type: dict
    batch_args = []  # type: list


def arg_val_ser(v):
    """serializer for command line arguments. This is required to profess
        True -> true
    for example."""
    if type(v) in [str, int, float, dict]:
        return str(v)
    elif type(v) is bool:
        return str(v).lower()
    elif type(v) in [list, tuple, set]:
        return ' '.join([arg_val_ser(i) for i in v])


### environment and command line argument serilizers
envs_serializer = lambda env: " ".join("{}={}".format(k, v) for k, v in env.items())
args_serializer = lambda kwargs: " ".join(
    "--{} {}".format(k.replace('_', '-'), arg_val_ser(v)) for k, v in kwargs.items())


def run(run_config: RunConfig):
    env_serialized = envs_serializer(run_config.env)
    hydrate_templates(run_config.args, RunTimeParams())
    args_serialized = args_serializer(run_config.args)
    script = run_config.run.format(args=args_serialized, env=env_serialized)
    print(script)

    try:
        check_call(script, shell=True)
    except Exception as e:
        print(e)

    logging.debug("escher.py-cli:env_serialized:{}".format(env_serialized), exc_info=False)
    logging.debug("escher.py-cli:args_serialized:{}".format(args_serialized), exc_info=False)
    logging.debug("escher.py-cli:job_script:{}".format(script), exc_info=False)


def job(run_config: RunConfig):
    if 'batch_args' in run_config:
        if ('args' in run_config) and run_config.args:
            logging.warning("both batch_args and args are defined. Only batch_args are used")
        batch_args = run_config.batch_args  # type: list
    else:
        if 'args' not in run_config:
            raise RuntimeError("Neither `batch_args` nor `args` is found in run_config, please check your config file.")
        batch_args = [vars(run_config.args)]  # type: list

    with_default = []
    for args in batch_args:
        c = deepcopy(run_config)
        c.args = deepcopy(run_config.default_args)
        c.args.update(**args)
        with_default.append(c)
    # this does not allow try multi-process.
    p = ProcessingPool(run_config.config.max_concurrent)
    p.map(run, with_default)


def main(config_file):
    """Escher-cli, a command line tool that helps with your ML experiments"""

    # logging.getLogger().setLevel(logging.DEBUG if debug else logging.INFO)
    # 1. take in yaml file, go through files and run one by one
    if config_file is None:
        raise EnvironmentError(f'need --config-file option')
    try:
        # noinspection PyUnresolvedReferences
        run_config = load_config(config_file)
        hydrated = DefaultBear(None, **{k: v for k, v in vars(RunConfig).items()
                                        if not is_hidden(k)})  # type: RunConfig
        hydrated.update(**run_config)
        job(hydrated)
    except Exception as e:
        raise EnvironmentError(f'config-file parse error', e)
