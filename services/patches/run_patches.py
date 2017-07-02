from dejavu import Dejavu
from patches import get_fingerprinted_songs


def run_patch_get_fingerprinted_song():
    """
    runs the patch for getting fingerprinted
    songs from the database
    """

    Dejavu.get_fingerprinted_songs = get_fingerprinted_songs


def run():
    """
    runs all the patches
    """

    run_patch_get_fingerprinted_song()
