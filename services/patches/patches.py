from dejavu.database import Database


def get_fingerprinted_songs(self):
    # get songs previously indexed
    self.songs = self.db.get_songs()
    self.songhashes_set = set()  # to know which ones we've computed before
    for song in self.songs:
        song_hash = song[Database.FIELD_FILE_SHA1]
        self.songhashes_set.add(song_hash)

    return self.songhashes
