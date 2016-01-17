from game import Game
import os

def par_dir():
    "Returns parent directory for this project"
    return os.path.dirname(os.path.realpath(__file__ + "/..") )
