from subprocess import check_call


def test_dave():
    check_call("cd test_project && dave --config-file=experiment.yml", shell=True)
