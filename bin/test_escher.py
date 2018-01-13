import sys
from subprocess import check_call, CalledProcessError


def test_escher():
    if sys.version_info >= (3, 6):
        print('python 3.6')
        try:
            check_call("cd ../test_project && source activate simulation && python "
                       "../bin/escher --config-file=experiment.yml", shell=True)
        except CalledProcessError as e:
            print(e)

