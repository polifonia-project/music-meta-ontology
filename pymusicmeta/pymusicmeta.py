"""
Create Music Knowledge Graphs via Python, using the Music Meta ontology.

Notes
-----
(*) Missing provenance information every time we add a triple; to be tested as
    an extension using RDF* (thea library). This has already been formnalised.
(*) Currently assumes that URIs are available, hence URI factories should be
    instantiated depending on the needs/requirements of users.

"""
from __future__ import annotations

import isodate
import logging
import argparse
from pathlib import Path
from typing import Union

from rdflib import Graph, Literal, Namespace, RDF, RDFS
from rdflib.namespace import XSD, URIRef
from tqdm import tqdm

from genres import MusicGenre

logger = logging.getLogger('musicmeta.create')

CORE = Namespace('http://w3id.org/polifonia/core/')
MM = Namespace('http://w3id.org/polifonia/music-meta/')
MR = Namespace('http://w3id.org/polifonia/music-representation/')


class URIFactory:

    def mint_from_string(self, str: str):
        raise NotImplementedError()

    def mint_from_file(self, str: Path):
        raise NotImplementedError()


class TripledObject():
    """
    General abstraction of a complex object that needs to be described by a
    number of triples providing complementary information. Utilities provide a
    way to streamline the creation and the manipulation of triples related to
    the object until they are added to a Graph.
    """
    def __init__(self, uri: str) -> None:
        self._uri = URIRef(uri)
        self._triple_store = []

    def update(self, subject, predicate, target):
        """Add a generic triple to this entity."""
        self._triple_store.append((subject, predicate, target))

    def supdate(self, predicate, target):
        """Add a triple to this object with URI as subject."""
        self._triple_store.append((self._uri, predicate, target))

    def set_uri(self, uri):
        """Set or rename the URI of this object if no triples created."""
        if len(self._triple_store) > 0:  # assumes at creation-time
            raise ValueError("Triples were already added")
        self._uri = uri

    def merge_to_graph(self, graph: Graph):
        """Add all triples of this object to the given graph."""
        for triple in self._triple_store:
            graph.add(triple)  # using graph as context


class Award(TripledObject):
    def __init__(self, uri: str, name: str = None, year: int = None) -> None:
        super().__init__(uri)


class MusicArtist(TripledObject):

    def __init__(self, uri, alias: Union[str, list] = None, genres: list = [],
                 influences: list = [], collaborators: list = []) -> None:
        """
        Creates a generic music artist from the given specifications. If a URI
        for the artist is not available, this should be created before calling
        this constructor via a `URIFactory`.

        Parameters
        ----------
        uri : str
            Universal Resource Identifier to use for this artist.
        alias : Union[str, list]
            A name for this artist, or a list of tuples where each record is of
            type (alias, language); language is left blank if not available.
        genres : list of str | list of `MusicGenre`, optional
            A list of music genres, preferably borrowed from a taxonomy.
        influences : list of str | list of `MusicArtist`, optional
            A list of influential artists (or agents) given as URIs.
        collaborators : list of str | list of `MusicArtist`, optional
            A list of collaborators (e.g. other artists/agents), given as URIs.

        """
        super(MusicArtist, self).__init__(uri)  # init triple object
        self.alias = alias  # FIXME
        self._genres = set()
        self._influences = set()
        self._collaborations = set()
        # Update the object and its triple store
        for genre in genres:
            self.add_genre(genre)
        for influence in influences:
            self.add_influence(influence)
        for collaborator in collaborators:
            self.add_collaboration(collaborator)
        self.activity = {"start": None, "end": None}
        # Minting a new URI if required: strategy to parameterise
        self.supdate(RDF.type, CORE.MusicArtist)
        # self.supdate(CORE.hasAlias, Literal(alias))  # FIXME

    def add_genre(self, genre:Union[MusicGenre, str]):
        genre_uri = genre._uri if isinstance(genre, MusicGenre) \
            else URIRef(genre)  # URI is retrieved from object or assumed
        self._genres.add(genre)
        self.supdate(MM.hasGenre, genre_uri)

    def add_influence(self, artist:Union[MusicArtist, str]):
        influence_uri = artist._uri if isinstance(artist, MusicArtist) \
            else URIRef(artist)  # URI is retrieved from object or assumed
        self._influences.add(artist)
        self.supdate(MM.isInfluencedBy, influence_uri)
        self.update(influence_uri, MM.influenced, self._uri)

    def add_collaboration(self, artist):
        collaborator_uri = artist._uri if isinstance(artist, MusicArtist) \
            else URIRef(artist)  # URI is retrieved from object or assumed
        self._collaborations.add(collaborator_uri)
        self.supdate(MM.hasCollaboratedWith, artist)
        # XXX if collabs are symmetric, then this triple is not needed
        self.update(collaborator_uri, MM.hasCollaboratedWith, self._uri)

    def add_activity(self, start_date, end_date=None):
        self.activity["start"] = start_date
        self.activity["end"] = end_date
        self.supdate(MM.activityStartDate,
                     Literal(start_date, datatype=XSD.date))
        if end_date is not None:  # an artist that is no longer active
            self.supdate(MM.activityEndDate,
                          Literal(end_date, datatype=XSD.date))

    def add_award(self, award: Union[str, Award], award_type="received"):
        if award_type == "received":
            self.supdate(MM.reicevedAward, award)
        elif award_type == "nominated":
            self.supdate(MM.nominatedForAward, award)
        else:  # cannot distinguish the award type associated to this artist
            raise ValueError(f"Not a supported award type: {award_type}")


class MusicEnsemble(MusicArtist):

    def __init__(self, uri, alias: str | list = None, genres: list = [],
                 influences: list = [], collaborators: list = [],
                 formation_place: str = None) -> None:
        super().__init__(uri, alias, genres, influences, collaborators)
        self.supdate(RDF.type, CORE.MusicEnsemble)
        self.add_formation_place(formation_place)
        self.members = []

    def add_formation_place(self, formation_place: str):
        if formation_place is not None:
            self.formation_place = formation_place
            self.supdate(MM.wasFormedIn, URIRef(formation_place))  # FIXME
    
    def add_artist(self, artist: Union[str, MusicArtist], ):
        pass


class MusicMetaGraph(Graph):
    """
    Extension of the rdflib `Graph` class to wrap a Music Meta Knowledge Graph.
    Elements of the graph are expected to be created apriori, using URIs.
    """

    def __init__(self, *args, **kwargs):
        super(MusicMetaGraph, self).__init__(*args, **kwargs)
        self.bind("mm", MM)

    def add_artist(self, artist: MusicArtist):
        """
        Add a music artist to the graph.
        """
        artist.merge_to_graph(self)
