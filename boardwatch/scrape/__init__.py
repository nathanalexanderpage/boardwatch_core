import sys
import pathlib
path_to_parent = str(pathlib.Path(__file__).resolve().parents[2].absolute())
sys.path.append(path_to_parent)
import boardwatch
