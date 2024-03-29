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
from exceptions import DuplicatedRecord
from utils import recontextaulise_uri


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
        if isinstance(alias, str):
            alias = Alias(alias)
        self._aliases.add(alias)
        self.supdate(CORE.hasAlias, alias._uri)

    def add_genre(self, genre:Union[MusicGenre, str]):
        if isinstance(genre, str):
            genre = MusicGenre(genre)
        self._genres.add(genre)
        self.supdate(MM.hasGenre, genre._uri)

    def add_influence(self, artist:Union[MusicArtist, str]):
        if isinstance(artist, str):
            artist = MusicArtist(artist)
        self._influences.add(artist)
        self.supdate(MM.isInfluencedBy, artist._uri)
        self.tupdate(artist._uri, MM.influenced)

    def add_collaboration(self, artist):
        collaborator_uri = get_uri(artist)
        self._collaborations.add(collaborator_uri)
        self.supdate(MM.hasCollaboratedWith, artist)
        # XXX if collabs are symmetric, then this triple is not needed
        self.tupdate(collaborator_uri, MM.hasCollaboratedWith)

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
    Therefore, it is intended to group Musicians and Music Algorithms.
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
        # Adding members requires creating memberships
        self._memberships = []
        for member in members:
            self.add_member(member)

    def add_formation_place(self, formation_place: Union[str, Place]):
        self._formation_place = formation_place
        self.supdate(MM.wasFormedIn, get_uri(formation_place))

    def add_member(self, artist: Union[str, Musician],
                   membership_start: str = None,
                   membership_end: str = None,
                   member_role: List[str] = []):
        """
        Add a music artist to the ensemble, with more granular control.
        A memembership URI is minted using the MusicEnsemble URI together with
        all the other specific information that is optionally provided.

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
        artist_uri = get_uri(artist)
        # Include the simple binary relations
        if artist_uri not in self._members:
            self.supdate(MM.hasMember, artist_uri)
            self.tupdate(artist_uri, MM.isMemberOf)
        # If more information is provided, we can create the membership
        membership_uri = recontextaulise_uri(
            self._uri, "MusicEnsembleMembership",
            artist_uri, membership_start, membership_end, member_role)

        membership_uri = URIRef(membership_uri)
        if membership_uri in self._memberships:
            raise DuplicatedRecord(f"Membership already exist: {membership_uri}")
        # Safe to go ahead and add membership-specific information
        self.update(membership_uri, RDF.type, MM.MusicEnsembleMembership)
        self.update(membership_uri, MM.involvesMusicEnsemble, self._uri)
        self.update(membership_uri, MM.hasMemberOfMusicEnsemble, artist_uri)

        if member_role is not None:
            self.update(membership_uri, CORE.involvesRole, URIRef(member_role))
        if membership_start is not None:
            timeinterval = TimeInterval(membership_start, membership_end)
            self.include_graph(timeinterval)  # add interval triples
            self.update(membership_uri, CORE.hasTimeInterval, timeinterval._uri)


class CreativeProcess(TripledObject):

    def __init__(self, uri: str,
                 authors: List[Union[str, MusicArtist]] = [],
                 author_roles: List[str] = [],
                 process_start_date: str = None,
                 process_end_date: str = None,
        ):
        super().__init__(uri)
        self.supdate(RDF.type, MM.CreativeProcess)
        no_author_roles = len(author_roles)
        if no_author_roles > 0:  # this is a shortcut thet expects alignment
            if no_author_roles > 0 and no_author_roles != len(authors):
                raise ValueError(f"Roles do not align with author list!")

        self.authors = set()
        self.creative_actions = list()
        for author, author_role in zip(authors, author_roles):
            self.add_author(author, roles=[author_role])

        process_timespan = TimeInterval(process_start_date, process_end_date)
        self.include_graph(process_timespan)  # add interval triples
        self.supdate(CORE.hasTimeInterval, process_timespan._uri)
        self.supdate(RDF.type, CORE.TimeIndexedSituation)

    def add_author(self, author: Union[str, URIRef, MusicArtist],
                   roles: List[Union[str, URIRef]] = []):
        """
        Add a music artist to the creative process, optionally with a role.

        Parameters
        ----------
        author : Union[str, MusicArtist]
            The music artists invovled in the creative process.
        role : list, optional
            The corresponding roles played by the given artists.
        """
        author_uri = get_uri(author)
        self.authors.add(author)  # remember the author
        self.supdate(CORE.involvesAgent, author_uri)
        self.tupdate(author_uri, CORE.isInvolvedIn)
        for role in roles:  # create n-ary relationship
            agent_role_uri = recontextaulise_uri(
                self._uri, "AgentRole", author_uri, role) # XXX Role URI
            self.update(agent_role_uri, RDF.type, CORE.AgentRole)
            self.update(agent_role_uri, CORE.involvesRole, role)
            self.update(agent_role_uri, CORE.involvesAgent, author_uri)
            self.supdate(CORE.hasAgentRole, agent_role_uri)

    def add_creative_action(self,
                            authors: List[Union[str, MusicArtist]] = [],
                            creative_tasks: List[str, URIRef] = [],
                            place: Union[str, Place] = None,
                            action_start_date: str = None,
                            action_end_date: str = None,
        ):
        # First running some sanity checks to make sure artists are not new
        for author in authors:
            if get_uri(author) not in [get_uri(a) for a in self.authors]:
                logger.warning(f"Artist {author} was not added as author!")
        # Second sanity check on the type of creative actions (if supported)
        resolved_tasks = []  # holding the URIs of the given creative tasks
        for task in creative_tasks:
            if isinstance(task, str):
                if task not in CREATIVE_TASKS:  # attempting to retrieve task
                    raise ValueError(f"Not a supported creative task {task}")
                task = CREATIVE_TASKS[task]  # retrieve the URI of the task
            resolved_tasks.append(task)

        # URI of CreativeAction can use the other optional info here and we
        # should check that at least some parameters are not None
        creative_action_uri = recontextaulise_uri(
                self._uri, "CreativeAction", *authors, *resolved_tasks,
                place, action_start_date, action_end_date)
        self.update(creative_action_uri, RDF.type, MM.CreativeAction)
        self.supdate(MM.involvesCreativeAction, creative_action_uri)

        if len(authors) > 0:
            for author in authors:
                self.update(creative_action_uri, CORE.involvesAgent, author)
        if len(resolved_tasks) > 0:
            for task in resolved_tasks:
                self.update(creative_action_uri, MM.executesTask, task)
        if place is not None:
            self.update(creative_action_uri, CORE.hasPlace, get_uri(place))
        if action_end_date is not None or action_end_date is not None:
            action_timespan = TimeInterval(action_end_date, action_end_date)
            self.include_graph(action_timespan)  # add interval triples
            self.supdate(CORE.hasTimeInterval, action_timespan._uri)


class MusicEntity(TripledObject):

    def __init__(self,
                uri : str,
                title: str,
                creative_process: CreativeProcess = None,
                genres: Union[List[str], List[MusicGenre]] = [],
                creators: Union[List[str], List[MusicArtist]] = []):
        """
        """
        super().__init__(uri)

        self.supdate(RDF.type, MM.MusicEntity)
        self.supdate(RDF.hasTitle, Literal(title, datatype=XSD.string))

        if creative_process is not None:
            creative_process.supdate(MM.creates, self._uri)
        for genre in genres:
            self.add_genre(genre)
        for artist in creators:
            self.tupdate(get_uri(artist), MM.isCreatorOf)


    def add_derivation(self, music_entity: Union[str, MusicEntity],
                       derivation_type: str):

        self.supdate(MM.isDerivedFrom, get_uri(music_entity))





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
