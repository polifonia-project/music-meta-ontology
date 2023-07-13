"""
Classes and utilities related to the Polifonia CORE ontology module and generala
abstractions to manipulate tripled objects.

See Also: https://github.com/polifonia-project/core-ontology
"""
import logging
from typing import Union
from dataclasses import dataclass
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
    the object until they are added to a Graph. Conceptually, this is akin to
    ``rdflib.Graph`` although the implementation here is streamlined.
    """
    def __init__(self, uri: str) -> None:
        self._uri = URIRef(uri)
        self._triple_store = set()

    def update(self, subject, predicate, target):
        """Add a generic triple to this entity."""
        if subject is None or target is None:
            logger.warn(f"Could not add triple {(subject, predicate, target)} "
                        f" -- subject or object is incomplete")
            return  # no triple is added and a logger warning is returned
        self._triple_store.add((subject, predicate, target))

    def supdate(self, predicate, target):
        """Add a triple to this object with URI as subject."""
        if target is None:
            logger.warn(f"Empty target for s-p ({self._uri, predicate})")
            return  # no triple is added and a logger warning is returned
        self._triple_store.add((self._uri, predicate, target))

    def set_uri(self, uri):
        """Set or rename the URI of this object if no triples created."""
        if len(self._triple_store) > 0:  # assumes at creation-time
            raise ValueError("Triples were already added")
        self._uri = uri

    def merge_to_graph(self, graph: Graph):
        """Add all triples of this object to the given graph."""
        for triple in self._triple_store:
            graph.add(triple)  # using graph as context

    def include_graph(self, graph):
        """Add all triples of the given graph object to this graph."""
        if isinstance(graph, TripledObject):
            triples = graph._triple_store
        elif isinstance(graph, Graph):
            triples = list(graph)
        else:  # not a valid input type
            raise ValueError(f"{type(graph)} graph type unsupported")
        for triple in triples:  # add triples one by one
            self._triple_store.add(triple)


class Alias(TripledObject):
    """An alias can be a single name, or can be decomposed into more names."""
    def __init__(self, uri: str, name: str, first_name: str = None,
                 last_name: str = None, language: str = None) -> None:
        super().__init__(uri)
        if not name and not (first_name or last_name):
            raise ValueError("At least a name or a decomposition is needed")
        self.supdate(CORE.hasLanguage, Literal(language, datatype=XSD.string))  # FIXME


@dataclass
class Place(TripledObject):
    """
    Encapsulates `https://w3id.org/polifonia/ontology/core/Place`
    TODO
    """
    name: str
    city: str
    country: str
    zipcode: str

    def __post_init__(self):
        self.supdate(RDF.type, CORE.Place)


@dataclass
class Person(TripledObject):
    """
    Encapsulates `https://w3id.org/polifonia/ontology/core/Person`
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
    def __init__(self, start_time: str, end_time: str,
                 subject: Union[str, TripledObject] = None) -> None:

        self._start_time = start_time
        self._end_time = end_time
        uri = URIRef(f"baseTODO/TimeInterval/{start_time}_{end_time}")
        super().__init__(uri=uri)  # FIXME
        self.supdate(RDF.type, CORE.TimeInterval)
        self.supdate(CORE.startTime, Literal(start_time, datatype=XSD.dateTime))
        self.supdate(CORE.endTime, Literal(end_time, datatype=XSD.dateTime))

        if subject is not None:  # attach to subject
            self.attach_to_subject(subject)
    
    def attach_to_subject(self, subject: Union[str, TripledObject]):
        """
        Associates this TimeInterval to the subject entity and updated the
        triple store of the latter if a `TripledObject` is passed.
        """
        self.update(get_uri(subject), CORE.hasTimeInterval, self._uri)
        if isinstance(subject, TripledObject):
            self.merge_to_graph(subject)  # add interval triples


def get_uri(entity: Union[str, TripledObject]):

    if isinstance(entity, str):  # here we assume that the string is the URI
        return URIRef(str)
    if isinstance(entity, TripledObject):  # here we retrieve the URI
        return entity._uri
    
    raise ValueError(f"Could not retrieve a URI from {type(entity)} object")

