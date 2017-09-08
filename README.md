# `Dave`, a command line utility that runs your script with arguments load from a Yaml file

:rocket::star:**Now `Dave` supports both python `3.5` and `3.6`!**:celebrate::collision:

`Dave` is a command line utility for your experiments. It manages concurrent runs, command line arguments and other stuff nicely for you!

The things it manages include:
- maximum concurrent runs (via python `multiprocess.Pool`)
- environment variables (env)
- default arguments
- batch arguments for multiple experiments

## Example Usage

First install via `pip` (it's that simple!!)

```bash
pip install dave
```

Suppose you have the following folder structure

```
└── MAML_tensorflow
    ├── README.md
    ├── experiment.yml
    ├── maml.py
    └── models
        ├── __init__.py
        └── mlp.py
```

where the experiment.yml file looks like this:

```yaml
%YAML 1.2
---
config:
  max_concurrent: 10
env:
  PYTHONPATH: test_directory
run: |
  {env} python maml_bradly.py {args}
default_args:
  npts: 100
  num_epochs: 70000
  num_tasks: 10
  num_grad_steps: 1
  num_points_sampled: 10
  fix_amp: False
batch_args: # use good typing convention here
  - num_tasks: 10
    num_grad_steps: 1
    num_points_sampled: 10
  - num_tasks: 10
    num_grad_steps: 4
    num_points_sampled: 20
tmp:
  - last_run: 10
```

Now under the project root, you can just run

```bash
dave --config-file "experiment.yml"
```

and it will automatically run the experiment twice, using the arguments in the `batch_args` field of the Yaml configuration file.
## To Develop

first download from github. Then under project folder, run (you also need to install the packages).

```bash
make dev test
```

### Bucket List

- [ ] Allow extensions
- [ ] work on windows
- [ ] allow env files

