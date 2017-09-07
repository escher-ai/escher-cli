import os
import sys

test_directory = os.getcwd()
assert test_directory in sys.path, "test_directory should be inside the system path."
