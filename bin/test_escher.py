import sys
from subprocess import check_call, CalledProcessError


def test_escher():
    try:
        check_call("cd ../test_project && source activate simulation && python "
                   "../bin/escher --config-file=scripts/test.escher", shell=True)
    except CalledProcessError as e:
        print(e)

