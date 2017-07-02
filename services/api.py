from flask import Flask
from patches.run_patches import run


app = Flask(__name__)


@app.route('/')
def index():
    return "Congratulations, you have reached the offplaylist server"


@app.route('/get-audio-fingerprint/', methods=['GET'])
def get_fingerprinted_audio_files():
    return "Hello World"


@app.route('/create-audio-fingerprint/', methods=['POST'])
def create_audio_fingerprint():
    return "Hello World"


if __name__ == "__main__":
    run()  # runs all the patches.
    app.run(debug=True)
