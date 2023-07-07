"""
Classes and utilities related to the Polifonia CORE ontology module and generala
abstractions to manipulate tripled objects.

See Also: XXX
"""
import logging
import dataclasses
from typing import List

from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import XSD, RDF

logger = logging.getLogger("pymusicmeta.corelib")
CORE = Namespace('http://w3id.org/polifonia/core/')


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
        self._triple_store.append((subject, predicate, target))  # None Check FIXME

    def supdate(self, predicate, target):
        """Add a triple to this object with URI as subject."""
        self._triple_store.append((self._uri, predicate, target))  # None Check FIXME

    def set_uri(self, uri):
        """Set or rename the URI of this object if no triples created."""
        if len(self._triple_store) > 0:  # assumes at creation-time
            raise ValueError("Triples were already added")
        self._uri = uri

    def merge_to_graph(self, graph: Graph):
        """Add all triples of this object to the given graph."""
        for triple in self._triple_store:
            graph.add(triple)  # using graph as context


class Alias(TripledObject):
    """An alias can be a single name, or can be decomposed into more names."""
    def __init__(self, uri: str, name: str, first_name: str = None,
                 last_name: str = None, language: str = None) -> None:
        super().__init__(uri)
        if not name and not (first_name or last_name):
            raise ValueError("At least a name or a decomposition is needed")
        self.supdate(CORE.hasLanguage, Literal(language, datatype=XSD.string))  # FIXME


@dataclasses
class Place(TripledObject):
    """
    TODO
    """
    name: str
    city: str
    country: str
    zipcode: str

    def __post_init__(self):
        self.supdate(RDF.type, CORE.Place)


@dataclasses
class Person(TripledObject):
    """
    TODO
    """
    bornPlace: Place
    bornName: Alias
    aliases: List[Alias]

    def __post_init__(self):
        self.supdate(RDF.type, CORE.Person)



class TimeInterval(TripledObject):
    """
    Encapsulates `https://w3id.org/polifonia/ontology/core/TimeInterval`
    
    FIXME again, the URI specification
    """
    def __init__(self, start_time: str, end_time: str) -> None:

        self._start_time = start_time
        self._end_time = end_time
        uri = URIRef(f"baseTODO/TimeInterval/{start_time}_{end_time}")
        super().__init__(uri=uri)  # FIXME
        self.supdate(RDF.type, CORE.TimeInterval)
        self.supdate(CORE.startTime, Literal(start_time, datatype=XSD.dateTime))
        self.supdate(CORE.endTime, Literal(end_time, datatype=XSD.dateTime))
        
