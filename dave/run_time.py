from datetime import datetime
from os import getcwd
from typing import TypeVar

from waterbear import Bear


# noinspection PyAbstractClass
class RunTimeParams(Bear):
    def __init__(self, **d):
        super().__init__(**d)
        # function is a bit limited, no access to {env}, no access to {args}
        self.time = datetime.now()
        self.cwd = getcwd()


T = TypeVar('T')


def hydrate_templates(g: T, params: RunTimeParams, update_global=True, recurse=True) -> (T, RunTimeParams):
    """Formats the namespace template strings, recurse by option, mutate runtime param with updated values.
    Goes through keys in order. (order is not stable or consistent in implementations).
    """
    for k, v in g.items():
        if hasattr(v, 'items') and recurse:
            # create a new local context so that lower level does not mutate global variable name.
            v, _ = hydrate_templates(v, dict(**vars(params)))
        if hasattr(v, 'format'):
            try:
                v = v.format(**params)
            except Exception as e:
                print(e)
        g[k] = v
        if update_global:
            params.update(**{k: v})

    return g, params
