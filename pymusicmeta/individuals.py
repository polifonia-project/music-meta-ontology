"""
Module wrapping the individuals currently supported in Music Meta.

"""
from rdflib import Namespace

CORE = Namespace('http://w3id.org/polifonia/core/')
MM = Namespace('http://w3id.org/polifonia/music-meta/')


CREATIVE_TASKS = {
    "lyrics_writing": MM.LyricsWriting,
    "music_writing": MM.MusicWriting,
    "instrumentation": MM.Instrumentation,  # XXX FIXME DUplicated in MMeta!
    "arrangement": MM.Arrangement,
    "orchestration": MM.Orchestration,
    "rearrangement": MM.Rearrangement,
    "remix": MM.Remix,
}
