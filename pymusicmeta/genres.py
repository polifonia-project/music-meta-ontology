"""
Utilities and abstractions to deal with music genres.
"""
from corelib import TripledObject

class MusicTag(TripledObject):

    def __init__(self, uri: str) -> None:
        super().__init__(uri)

    def get_name(self):
        pass


class MusicGenre(MusicTag):

    def get_name(self):
        pass

    def get_taxonomy(self):
        pass

    def validate(self):
        pass