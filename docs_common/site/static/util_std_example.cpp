import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[0])) 
from cpp_build import *

cpp_files = [path_traverse_up(__file__, 0) + "/main.cpp"]
output_dir = 
build_setup = BuildSetup(cpp_file_paths=cpp_files, output_file=)
build_setup.include_opengl()

build_setup.build_and_run()