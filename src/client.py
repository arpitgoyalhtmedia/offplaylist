from dejavu import Dejavu
from settings import config
from src.patches.run_patches import run


def run_client():
    """
    runs all the patches
    """
    run()
    directory_path = raw_input("enter the directory path")

    djv = Dejavu(config)
    djv.fingerprint_directory(directory_path, [".mp3"], 3)
