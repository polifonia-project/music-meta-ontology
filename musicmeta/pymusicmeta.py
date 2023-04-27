"""
An easy to use Python library for creating Music Knowledge Graphs using the
Music Meta ontology.

"""
from __future__ import annotations

import logging
import argparse
from pathlib import Path
from typing import Union

import joblib
import rdflib
from rdflib import Graph, Literal, Namespace, RDF, RDFS
from rdflib.namespace import XSD
from tqdm import tqdm

logger = logging.getLogger('musicmeta.create')

CORE = Namespace('http://w3id.org/polifonia/core/')
MM = Namespace('http://w3id.org/polifonia/music-meta/')
MF = Namespace('http://w3id.org/polifonia/music-representation/')


class URIFactory:

    def mint_from_string(self, str: str):
        raise NotImplementedError()

    def mint_from_file(self, str: Path):
        raise NotImplementedError()


class TripledObject():
    def __init__(self, uri: str = None) -> None:
        self._uri = uri
        self._triple_store = []

    def update(self, subject, predicate, target):
        """Add a generic triple to this entity."""
        self._triple_store.append(subject, predicate, target)

    def supdate(self, predicate, target):
        """Add a triple to this object with URI as subject."""
        self._triple_store.append(self._uri, predicate, target)

    def set_uri(self, uri):
        """Set or rename the URI of this object if no triples created."""
        if len(self._triple_store) > 0:  # assumes at creation-time
            raise ValueError("Triples were already added")
        self._uri = uri

    def merge_to_graph(self, graph: Graph):
        """Add all triples of this object to the given graph."""
        for triple in self._triple_store:
            graph.add(triple)  # using graph as context


class MusicArtist(TripledObject):

    def __init__(self, name: Union[str, dict], genre: str = None, ) -> None:
        super(MusicArtist, self).__init__()
        self.name = name
        self.genre = genre
        self.influences = []
        self.collaborations = []
        self.activity = {"start": None, "end": None}
        # Minting a new URI if required: strategy to parameterise
        self.artist_uri = MM[name] + "_XXX"  # FIXME
        self.supdate((RDF.type, CORE.MusicArtist))
        self.supdate((CORE.hasName, Literal(name)))  # FIXME
        self.supdate((MM.hasGenre, Literal(genre)))  # FIXME

    def add_influence(self, artist:Union[MusicArtist, str]):
        self.influences.append(artist)
        self.update((self.artist_uri, MM.isInfluencedBy, Literal(artist)))

    def add_collaboration(self, artist):
        self.collaborations.append(artist)
        self.update((self.artist_uri, MM.hasCollaboratedWith, Literal(artist)))

    def add_activity(self, start_date, end_date=None):
        self.activity["start"] = start_date
        self.activity["end"] = start_date
        self.update((self.artist_uri, MM.activityStartDate,
                     Literal(start_date, XSD.date)))
        if end_date is not None:
            self.update((self.artist_uri, MM.hasCollaboratedWith,
                         Literal(end_date, XSD.date)))

    def add_award(award, award_type="received"):
        if award_type not in ["nominated", "received"]:
            raise ValueError(f"Not a supported award type: {award_type}")


class MusicEnsemble(MusicArtist):

    def __init__(self, name: Union[str, dict], genre: str = None,
                 formation_place: str = None) -> None:
        super().__init__(name, genre)
        self.formation_place = formation_place


class MusicMetaGraph(Graph):
    """
    Extension of the rdflib `Graph` class to streamline the creation of Music
    Knowledge Graphs via the `musicmeta` library.
    """

    def __init__(self, *args, **kwargs):
        super(MusicMetaGraph, self).__init__(*args, **kwargs)

    def add_artist(self, artist: MusicArtist):
        """
        Add a music artist to the graph.
        """
        # FIXME this is a construct to generalise
        for triple in artist.triple_store:
            self.add(triple)
