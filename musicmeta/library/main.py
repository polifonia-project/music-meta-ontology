"""

"""

from rdflib import Graph


class MusicMetaGraph(Graph):
    """
    Extension of the rdflib Graph class to provide additional functionality
    specific to the MusicMeta library.
    """

    def __init__(self, *args, **kwargs):
        super(MusicMetaGraph, self).__init__(*args, **kwargs)

    def add_composer(self, composer):
        """
        Add a composer to the graph.
        """
        pass
