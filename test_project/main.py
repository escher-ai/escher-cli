import argparse
import os
import sys
from time import sleep

from moleskin import Moleskin

M = Moleskin()

test_directory = os.getcwd()
assert test_directory in sys.path, "test_directory should be inside the system path."

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--num-tasks', type=int)
parser.add_argument('--num-grad-steps', type=int)
parser.add_argument('--num-points-sampled', type=int)
parser.add_argument('--run-id', type=str)

args, unknown_args = parser.parse_known_args()
M.yellow(args, unknown_args)
M.green(args.run_id)
try:
    assert args.num_tasks == 20
    assert args.num_grad_steps == 3
    assert args.num_points_sampled == 50
except AssertionError as e:
    assert args.num_tasks == 10
    assert args.num_grad_steps == 1
    assert args.num_points_sampled == 10

sleep(0.5)
