import sys
import pathlib
path_to_root = str(pathlib.Path(__file__).resolve().parents[1].absolute())
sys.path.append(path_to_root)
import boardwatch
