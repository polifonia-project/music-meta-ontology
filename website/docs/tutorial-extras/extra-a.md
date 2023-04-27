---
sidebar_position: 1
---

# Introduction to pyMusicMeta

To facilitate the reuse of Music Meta and its data conversion into OWL/RDF Knowledge Graph, we developed a library to map arbitrary music metadata into RDF triples.
This enables a practical and scalable workflow for data lifting to create Music Knowledge Graphs without expert knowledge of our ontological model.
The library is developed in Python as an extension of RDF-Lib \cite{bottinger2018rdflib}.

The Music Meta library allows for the creation of RDF triples from textual data, offering the advantage of easy data generation using our model.
The library provides a range of simple methods for adding triples to a graph, using clear, concise documentation and straightforward naming conventions.
With each triple added, the library automatically adds alignments to other schema that Music Meta supports, thus bringing interoperability with ontologies.