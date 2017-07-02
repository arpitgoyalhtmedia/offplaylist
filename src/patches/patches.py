import dejavu.decoder as decoder
import multiprocessing
import traceback
import sys
from settings import BATCH_NUMBER
from src.utils import call_fingerprint_create_api
import os
from dejavu import fingerprint


def fingerprint_directory(self, path, extensions, nprocesses=None):
    # Try to use the maximum amount of processes if not given.
    try:
        nprocesses = nprocesses or multiprocessing.cpu_count()
    except NotImplementedError:
        nprocesses = 1
    else:
        nprocesses = 1 if nprocesses <= 0 else nprocesses

    pool = multiprocessing.Pool(nprocesses)

    filenames_to_fingerprint = []
    for filename, _ in decoder.find_files(path, extensions):
        filenames_to_fingerprint.append(filename)

    # Prepare _fingerprint_worker input
    worker_input = zip(filenames_to_fingerprint,
                       [self.limit] * len(filenames_to_fingerprint))

    # Send off our tasks
    iterator = pool.imap_unordered(_fingerprint_worker,
                                   worker_input)

    # Loop till we have all of them
    batch_list = []
    while True:
        try:
            song_name, hashes, file_hash, filename = iterator.next()
            hashes_list = list(hashes)
        except multiprocessing.TimeoutError:
            continue
        except StopIteration:
            break
        except:
            print("Failed fingerprinting")
            # Print traceback because we can't reraise it here
            traceback.print_exc(file=sys.stdout)
        else:
            batch_list.append({
                "song_name": song_name,
                "hashes_list": hashes_list,
                "file_hash": file_hash,
                "filename": filename,
            })

            if len(batch_list) == BATCH_NUMBER:
                call_fingerprint_create_api(batch_list)
                batch_list = []

    if len(batch_list) < BATCH_NUMBER:
        call_fingerprint_create_api(batch_list)

    pool.close()
    pool.join()


def _fingerprint_worker(filename, limit=None, song_name=None):
    # Pool.imap sends arguments as tuples so we have to unpack
    # them ourself.
    try:
        filename, limit = filename
    except ValueError:
        pass

    songname, extension = os.path.splitext(os.path.basename(filename))
    song_name = song_name or songname
    channels, Fs, file_hash = decoder.read(filename, limit)
    result = set()
    channel_amount = len(channels)

    for channeln, channel in enumerate(channels):
        # TODO: Remove prints or change them into optional logging.
        print("Fingerprinting channel %d/%d for %s" % (channeln + 1,
                                                       channel_amount,
                                                       filename))
        hashes = fingerprint.fingerprint(channel, Fs=Fs)
        print("Finished channel %d/%d for %s" % (channeln + 1, channel_amount,
                                                 filename))
        result |= set(hashes)

    return song_name, result, file_hash, filename
