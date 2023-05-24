---
component-id: pymusicmeta
type: Software
name: pymusicmeta
description: A library to create Music Meta resources on the Web.
logo: website/static/img/musicmeta_logo.png
work-package:
- WP2
pilot:
- INTERLINK
- TUNES
- FACETS
- TONALITIES
project: polifonia-project
resource: https://github.com/polifonia-project/music-meta-ontology/tree/main/musicmeta
release-date: 13/04/2023
release-number: v1.0
release-link: https://github.com/polifonia-project/music-meta-ontology
doi: 10.5281/zenodo.7919970
changelog: https://github.com/polifonia-project/music-meta-ontology
licence:
- IscLicense
copyright: "Copyright (c) 2023 Music Meta Contributors"
contributors: # replace these with the GitHub URL of each contributor
- Jacopo de Berardinis <https://github.com/jonnybluesman>
- Andrea Poltronieri <https://github.com/andreamust>
related-components:
- informed-by:
  - https://w3id.org/polifonia/ontology/music-meta/
- reuses:  # any reused/imported ontology
  - https://w3id.org/polifonia/ontology/music-meta/
- documentation:  # link any resource providing documentation for this ontology
  - https://w3id.org/polifonia/ontology/music-meta/
---

# pymusicmeta

To facilitate the reuse of Music Meta and its data conversion into OWL/RDF
Knowledge Graph, we developed a library to map arbitrary music metadata into RDF
triples. This enables a practical and scalable workflow for data lifting to
create Music Knowledge Graphs without expert knowledge of our ontological model.
The library is developed in Python as an extension of RDF-Lib.

The Music Meta library allows for the creation of RDF triples from textual data,
offering the advantage of easy data generation using our model. The library
provides a range of simple methods for adding triples to a graph, using clear,
concise documentation and straightforward naming conventions. With each triple
added, the library automatically adds alignments to other schema that Music Meta
supports, thus bringing interoperability with ontologies.

[Link to the website](https://github.com/polifonia-project/music-meta-ontology)