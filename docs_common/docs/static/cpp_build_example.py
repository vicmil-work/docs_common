import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[0])) 
from cpp_build import *

"""
In order to run, ensure you have a valid compiler installed
for windows, download into: ./deps/mingw64
for linux: sudo apt install gcc
"""

cpp_files = [path_traverse_up(__file__, 0) + "/main.cpp"]
build_setup = BuildSetup(cpp_file_paths=cpp_files)

build_setup.build_and_run()