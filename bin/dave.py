"""Example script
glow --config-file="experiment.yaml" --starting-index=0 --
"""
from pathos.multiprocessing import ProcessingPool
from pathlib import Path
from subprocess import check_call

from munch import DefaultMunch, Munch
from ruamel.yaml import YAML

from params_proto import cli_parse, ParamsProto


@cli_parse
class Experiment(ParamsProto):
    """Supervised MAML in tensorflow"""
    # config_file = './experiment.yml',  # type: "configuration of the experiment"
    # starting_index = None,  # type: "hashed or integer index for the starting experiment"
    config_file: "configuration of the experiment" = './experiment.yml'
    starting_index: "hashed or integer index for the starting experiment" = 0


class RunnerConfig:
    max_concurrent: int = 4


class RunConfig:
    config: RunnerConfig = DefaultMunch(None)
    run: str = 'python main.py {args}'
    default_args: dict = {}
    args: dict = {}
    batch_args: list = []


args_serializer = lambda kwargs: " ".join("--{} {}".format(k.replace('_', '-'), v) for k, v in kwargs.items())


def job(config: RunConfig):
    def run(args):
        args_hydrated = Munch(config.default_args)
        args_hydrated.update(vars(args))
        args_serialized = args_serializer(args_hydrated)
        script = config.run.format(args=args_serialized)
        check_call(script)

    args = config.batch_args or [config.args]
    p = ProcessingPool(config.config.max_concurrent)
    p.map(run, args)


# 1. take in yaml file, go through files and run one by one
yaml = YAML(typ='unsafe', pure=True)
for config in yaml.load_all(Path(Experiment.config_file)):
    job(Munch.fromDict(config))
