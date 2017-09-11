import argparse
import os
import sys

test_directory = os.getcwd()
assert test_directory in sys.path, "test_directory should be inside the system path."

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--num-tasks', type=int)
parser.add_argument('--num-grad-steps', type=int)
parser.add_argument('--num-points-sampled', type=int)

args, unknow_args = parser.parse_known_args()
assert args.num_tasks == 20
assert args.num_grad_steps == 3
assert args.num_points_sampled == 50
