from settings import HTTP_HOST
import json
import requests
from threading import Timer
from multiprocessing import RawValue, Lock


def call_fingerprint_create_api(batch):
    """
    calls the fingerprint creation api for the
    main server that hosts all the data
    """
    URL = HTTP_HOST + "/create-audio-fingerprint/"
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(
        URL,
        json.dumps(batch),
        headers=headers
    )

    if response.status_code == 400:
        print "Bad Request"


class Counter(object):
    def __init__(self, value=0):
        self.val = RawValue('i', value)
        self.lock = Lock()

    def increment(self):
        with self.lock:
            self.val.value += 1

    def value(self):
        with self.lock:
            return self.val.value


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
