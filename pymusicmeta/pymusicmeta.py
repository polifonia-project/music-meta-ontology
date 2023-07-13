"""
Create Music Meta Knowledge Graphs via Python, using the Music Meta ontology.

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
import dataclasses
from pathlib import Path
from typing import Union, List

from tqdm import tqdm
from rdflib import Graph, Literal, Namespace, RDF, RDFS, XSD, URIRef

from corelib import TripledObject, Place, Person, Alias, TimeInterval, get_uri
from individuals import CREATIVE_TASKS
from genres import MusicGenre


logger = logging.getLogger('musicmeta.create')

CORE = Namespace('http://w3id.org/polifonia/core/')
MM = Namespace('http://w3id.org/polifonia/music-meta/')
MR = Namespace('http://w3id.org/polifonia/music-representation/')


class Award(TripledObject):
    """An award comes with title and year specification."""
    def __init__(self, uri: str, title: str = None, year: int = None) -> None:
        super().__init__(uri)
        self.supdate(CORE.hasTitle, Literal(title, datatype=XSD.string))
        self.supdate(CORE.hasYear, Literal(year, datatype=XSD.year))  # FIXME
        # TODO An award may have more information/details to include


class MusicArtist(TripledObject):

    def __init__(self,
                 uri : str,
                 activity_start_date: str = None,
                 activity_end_date: str = None,
                 aliases: Union[List[str], List[Alias]] = [],
                 genres: Union[List[str], List[MusicGenre]] = [],
                 influences: Union[List[str], List[MusicArtist]] = [],
                 collaborators: Union[List[str], List[MusicArtist]] = []):
        """
        Creates a generic music artist from the given specifications. If a URI
        for the artist is not available, this should be created before calling
        this constructor via a specialisation of `URIFactory`.

        Parameters
        ----------
        uri : str
            Universal Resource Identifier to use for this artist.
        aliases : Union[List[str], List[Alias]]
            A list of aliases for this artist, given as URIs or Alias(es).
        genres : list of str | list of `MusicGenre`, optional
            A list of music genres, given as URIs or MusicGenre(s)
        influences : list of str | list of `MusicArtist`, optional
            A list of influential artists given as URIs or MusicArtist(s).
        collaborators : list of str | list of `MusicArtist`, optional
            A list of influential collaborators given as URIs or MusicArtist(s).

        Note: AgentRole, Role are still missing in the current implementation.
        """
        super(MusicArtist, self).__init__(uri)  # init triple object
        self._activity = dict()
        self._aliases = set()
        self._genres = set()
        self._influences = set()
        self._collaborations = set()
        # Update the object and its triple store
        for alias in aliases:
            self.add_alias(alias)
        for genre in genres:
            self.add_genre(genre)
        for influence in influences:
            self.add_influence(influence)
        for collaborator in collaborators:
            self.add_collaboration(collaborator)
        self.add_activity(activity_start_date, activity_end_date)
        # Minting a new URI if required: strategy to parameterise
        self.supdate(RDF.type, CORE.MusicArtist)

    def add_alias(self, alias:Union[Alias, str]):
        alias_uri = alias._uri if isinstance(alias, Alias) \
            else URIRef(alias)  # URI is retrieved from object or assumed
        self._aliases.add(alias)
        self.supdate(CORE.hasAlias, alias_uri)

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
        if start_date is not None:
            self._activity["start"] = start_date
            self._activity["end"] = end_date
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


class Musician(MusicArtist, Person):
    """
    A Musician is a both a MusicArtist and a Person (CORE).

    Notes
    -----
    - At the current stage, as per MM, we do not have particular properties
        extending the specialisation of musician, though we plan to support them
        e.g. the ability to use a medium of performance, musical training, etc.

    See also
    --------
    - https://github.com/polifonia-project/core-ontology

    """
    def __init__(self, uri: str, **kwargs):
        super().__init__(uri, **kwargs)
        self.supdate(RDF.type, MM.Musician)


class MusicAlgorithm(MusicArtist):
    """
    A MusicAlgorithm is a specialisation MusicArtist with additional properties
    that can be registered using the `music-algorithm` and `cometa` ontologies.

    See also
    --------
    - https://github.com/polifonia-project/cometa-ontology
    - https://github.com/polifonia-project/music-algorithm-ontology
    
    """
    def __init__(self, uri: str,
                 dataset: str = None, **kwargs):
        super().__init__(uri, **kwargs)
        self.supdate(RDF.type, MM.MusicAlgorithm)
        if dataset is not None:
            self.update(URIRef(dataset), RDF.type, MM.MusicDataset)
            self.supdate(MM.isTrainedON, URIRef(dataset))


class MusicEnsemble(MusicArtist):
    """
    A MusicEnsemble generalises over groups, ensembles, orchestras, choirs, etc.
    Therefore, it is intended to group Musicians.

    """
    def __init__(self, uri: str,
                 formation_place: Union[str, Place] = None,
                 members: List[Union[str, MusicArtist]] = [], **kwargs):
        """
        Creates a music ensemble with basic information.
        """
        super().__init__(uri, **kwargs)
        self._members = members
        self.supdate(RDF.type, MM.MusicEnsemble)
        self.add_formation_place(formation_place)
        for member in members:
            self.add_member(member)

    def add_formation_place(self, formation_place: str):
        self._formation_place = formation_place
        self.supdate(MM.wasFormedIn, URIRef(formation_place))

    def add_member(self, artist: Union[str, Musician],
                   membership_start: str = None,
                   membership_end: str = None,
                   member_role: List[str] = []):
        """
        Add a musician to the ensemble.

        Parameters
        ----------
        artist : Union[str, Musician]
            Either the URI or the relevant class of the member. 
        membership_start : str, optional
            The date when the artist joined the ensemble, if available.
        membership_end : str, optional
            The data when the artist left the ensemble, if applicable.
        member_role : str, optional
            The URI of the role of the artist, e.g. a singer role.

        Note: a member can have more than 1 role.
        """
        artist_uri = artist._uri if isinstance(artist, MusicArtist) \
            else URIRef(artist)  # URI is retrieved from object or assumed
        # Include the simple binary relations first
        self.supdate(MM.hasMember, artist_uri)
        self.update(artist_uri, MM.isMemberOf, self._uri)
        # If more information is provided, we can create the membership
        # FIXME At the moment the membership URI is based on a simple concat
        membership_uri = f"Base_resoruce_URI_(TODO)_/MusicEnsembleMembership" \
                         f"/{self._uri.split('/')[-1]}" \
                         f"_{artist_uri.split('/')[-1]}"
        for memb_detail in [membership_start, membership_end, member_role]:
            if memb_detail is not None:
                pass # membership_uri += memb_detail if

        membership_uri = URIRef(membership_uri)
        self.update(membership_uri, RDF.type, MM.MusicEnsembleMembership)
        self.update(membership_uri, MM.involvesMusicEnsemble, self._uri)
        self.update(membership_uri, MM.hasMemberOfMusicEnsemble, artist_uri)
  
        if member_role is not None:
            self.update(membership_uri, CORE.involvesRole, URIRef(member_role))
        if membership_start is not None:
            timeinterval = TimeInterval(membership_start, membership_end)
            self.include_graph(timeinterval)  # add interval triples
            self.update(membership_uri, CORE.hasTimeInterval, timeinterval._uri)


class CreationProcess(TripledObject):

    def __init__(self, uri: str,
                 authors: List[Union[str, MusicArtist]]=None,
                 author_roles: List[str] = None,
                 process_start_date: str = None,
                 process_end_date: str = None,
        ):
        super().__init__(uri)

        if author_roles is not None:
            if len(author_roles) != len(authors):
                raise ValueError(f"Roles do align with author list!")
        else:  # creating an empty list of roles
            author_roles = [None] * len(authors)

        self.authors = set()
        self.creative_actions = list()
        for author, author_role in zip(authors, author_roles):
            self.add_author(author, role=author_role)
        
        process_timespan = TimeInterval(process_start_date, process_end_date)
        self.include_graph(process_timespan)  # add interval triples
        self.update(self._uri, CORE.hasTimeInterval, process_timespan._uri)

    def add_author(self, author: Union[str, MusicArtist], role: str = None):
        """
        XXX Author is Agent in the most general sense, not just music artist!

        """
        author_uri = get_uri(author)
        self.authors.add(author)  # remember the author
        self.supdate(CORE.involvesAgent, author_uri)
        self.update(author_uri, CORE.isInvolvedIn, self._uri)
        if role is not None:  # create n-ary relationship
            agent_role_uri = "creative_process_plus_agent_plus_role_TODO"  #TODO
            self.update(agent_role_uri, RDF.type, CORE.AgentRole)
            self.update(agent_role_uri, CORE.involvesRole, role)
            self.update(agent_role_uri, CORE.involvesAgent, author_uri)
            self.supdate(CORE.hasAgentRole, agent_role_uri)
    
    def add_creative_action(self,
                            authors: List[Union[str, MusicArtist]] = None,
                            creative_tasks: List[str] = None,
                            place: Union[str, Place] = None,
                            action_start_date: str = None,
                            action_end_date: str = None,
        ):
        if not all([c for c in creative_tasks]):  # sanity check on CTs
            raise ValueError(f"Supported creative tasks: {CREATIVE_TASKS}")

        # URI of CreativeAction can use the other optional info here and we
        # should check that at least some parameters are not None
        creative_action_uri = self.uri + "_some_incremental_suffix"  # FIXME
        self.update(creative_action_uri, RDFS.subClassOf, CORE.TimeIndexedSituation)

        if authors is not None:
            for author in authors:
                self.update(creative_action_uri, CORE.involvesAgent, author)



class MusicMetaGraph(Graph):
    """
    Extension of the rdflib `Graph` class to wrap a Music Meta Knowledge Graph.
    Elements of the graph are expected to be created apriori, using URIs.
    """
    def __init__(self, *args, **kwargs):
        super(MusicMetaGraph, self).__init__(*args, **kwargs)
        self.bind("mm", MM)

    def add_tripled_object(self, tripled_object: TripledObject):
        """
        Add a `TripledObject` to this graph.
        """
        tripled_object.merge_to_graph(self)
