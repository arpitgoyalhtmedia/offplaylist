from flask import Flask, jsonify, request, abort
from patches.run_patches import run
from settings import config
from dejavu import Dejavu
import dejavu.decoder as decoder


app = Flask(__name__)


@app.route('/')
def index():
    return "Congratulations, you have reached the offplaylist server"


@app.route('/get-audio-fingerprint/', methods=['GET'])
def get_fingerprinted_audio_files():
    djv = Dejavu(config)
    songhashes_list = list(djv.songhashes_set)

    return jsonify(songhashes_list)


@app.route('/create-audio-fingerprint/', methods=['POST'])
def create_audio_fingerprint():
    djv = Dejavu(config)

    if not request.json:
        abort(400)

    filtered_values = []

    for datum in request.json:
        if decoder.unique_hash(datum.get("filename")) in djv.songhashes_set:
            print "{} already fingerprinted, continuing...".format(
                datum.get("filename")
            )
        else:
            filtered_values.append(datum)
            djv.get_fingerprinted_songs()

    for batch in request.json:
        sid = djv.db.insert_song(
            batch.get("song_name"),
            batch.get("file_hash")
        )
        djv.db.insert_hashes(sid, set(batch.get("hashes_list")))
        djv.db.set_song_fingerprinted(sid)


def run_server():
    run()  # runs all the patches.
    app.run(host="0.0.0.0", debug=False)
