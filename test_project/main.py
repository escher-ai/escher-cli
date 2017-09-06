import sys

print(sys.path)
assert "test_directory" in sys.path, "test_directory should be inside the system path."
