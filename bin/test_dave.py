import sys
from subprocess import check_call, CalledProcessError


def test_dave_36():
    if sys.version_info >= (3, 6):
        print('python 3.6')
        try:
            check_call("cd ../test_project && source activate simulation && python "
                       "../bin/dave --config-file=experiment.yml", shell=True)
        except CalledProcessError as e:
            print(e)


def test_dave_35():
    if sys.version_info < (3, 6):
        print('python 3.5')
        try:
            check_call("cd ../test_project && source activate gym && python "
                       "../bin/dave --config-file=experiment.yml", shell=True)
        except CalledProcessError as e:
            print(e)
