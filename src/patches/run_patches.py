from dejavu import Dejavu
import dejavu
from patches import fingerprint_directory, _fingerprint_worker


def run_patch_fingerprint_directory():
    """
    patches the fingerprint directory
    function
    """

    Dejavu.fingerprint_directory = fingerprint_directory


def run_patch_fingerprint_worker():
    """
    patches the fingerprint worker
    function
    """

    dejavu._fingerprint_worker = _fingerprint_worker


def run():
    """
    runs all the patches
    """

    run_patch_fingerprint_directory()
    run_patch_fingerprint_worker()
