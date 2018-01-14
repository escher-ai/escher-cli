import argparse
import os
import sys
from distutils import util
from time import sleep

from moleskin import Moleskin
from pathos.multiprocessing import ProcessingPool

M = Moleskin()

test_directory = os.getcwd()
assert test_directory in sys.path, "test_directory should be inside the system path."

_bool = lambda v: bool(util.strtobool(v))

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--run-id', type=str)
parser.add_argument('--default-int', type=int)
parser.add_argument('--default-bool', type=_bool)
parser.add_argument('--nargs-bool', type=_bool, nargs="*")
parser.add_argument('--nargs-int', type=int, nargs="*")
parser.add_argument('--nargs-str', type=str, nargs="*")


def ProcFn(i):
    def proc_fn():
        print(f' ==> process function {i}')
        sleep(20)


def fork_process():  # tests if process can have subprocess
    p = ProcessingPool(10)
    for i in range(10):
        p.map(ProcFn(i), [])


args, unknown_args = parser.parse_known_args()
M.print()
M.print(args, unknown_args)

M.print(args.run_id)
assert args.run_id == "test"
M.print(args.default_int)
assert args.default_int == 10
M.print(args.default_bool)
assert args.default_bool == False
M.print(args.nargs_bool)
assert args.nargs_bool == [True, False]
M.print(args.nargs_int)
assert args.nargs_int == [10, 100]
M.print(args.nargs_str)
assert args.nargs_str == ["some", "thing"]

print("✓")

# test forking processes
print('forking process')
fork_process()
sleep(1)  # wait before termination to show up in `htop`.
