---
component-id: https://w3id.org/polifonia/ontology/music-meta/
type: Ontology
name: Music Meta
description: An ontology to describe music metadata
image: diagrams/music_meta.png
logo: website/static/img/musicmeta_logo.png
work-package:
- WP2
pilot:
- INTERLINK
- TUNES
- FACETS
- TONALITIES
project: polifonia-project
resource: ontology/musicmeta.owl
release-date: 13/04/2023
release-number: v1.0
release-link: https://github.com/polifonia-project/ontology-network/releases
doi: 10.5281/zenodo.7919970
changelog: https://github.com/polifonia-project/ontology-network/releases
licence: 
- CC-BY_v4
copyright: "Copyright (c) 2023 My Ontology Contributors"
contributors: # replace these with the GitHub URL of each contributor
- Jacopo de Berardinis <https://github.com/jonnybluesman>
- Andrea Poltronieri <https://github.com/andreamust>
- Valentina Anita Carriero <https://github.com/valecarriero>
- Nicolas Lazzari <https://github.com/n28div>
- Peter van Kranenburg <https://github.com/pvankranenburg>
- Philippe Rigaux <https://github.com/rigaux>
- Mari Wigham <https://github.com/mwigham>
- Marco Gurrieri <https://github.com/margur78>
related-components:
- informed-by:
  - https://github.com/polifonia-project/polifoniacq-dataset
- reuses:  # any reused/imported ontology
  - https://github.com/polifonia-project/core/
- story:  # any related story this ontology addresses
  - https://github.com/polifonia-project/stories/blob/main/Linka_Computer_Scientist/Linka%231_MusicKnowledge.md
- persona:  # any persona this ontology addresses
  - https://github.com/polifonia-project/stories/tree/main/Linka_Computer_Scientist
- documentation:  # link any resource providing documentation for this ontology
  - https://polifonia-project.github.io/music-meta-ontology/
---

<!-- bibliography:
- main-publication: "Author 1, Author 2, and Author 3. \"Title of publication\"
in My Journal or Conference (2023): 1-31. https://dl.ac.org/doi/pdf/XXX.YYY"
- publication:
  - "Author 1, Author 2, and Author 3. \"Another title of publication\"
in My Journal or Conference (2023): 1-31. https://dl.ac.org/doi/pdf/XXX.YYY"
  -  "Author 1, Author 2, and Author 3. \"Again another title of publication\"
in My Journal or Conference (2023): 1-31. https://dl.ac.org/doi/pdf/XXX.YYY"
- deliverable-document:
  - "Author 1, Author 2, and Author 3. \"Another title of publication\"
in My Journal or Conference (2023): 1-31. https://dl.ac.org/doi/pdf/XXX.YYY" -->

# Music Meta Ontology

The Music Meta module provides a rich and flexible ontology to describe music
metadata related to artists, compositions, performances, recordings,
casts, and links. Music Meta focuses on provenance and interoperability – 
essential requirements for the integration of music datasets, which is currently
hampered by the specificity of existent ontologies. The model is based on the
Information-Realisation ODP, allowing to reduce complexity of FRBR-based
models, whose application in the music domain has raised concerns.
To enable data integration from existing knowledge bases and datasets, we also
align Meta to Music Ontology, DOREMUS, and Wikidata. To facil- itate
the reuse of Music Meta and its data conversion into OWL/RDF Knowl- edge Graphs,
we developed a library to map arbitrary music metadata into RDF triples. This
enables a practical and scalable workflow for data lifting to create Music
Knowledge Graphs without expert knowledge of our ontological model.

[Link to the website](https://github.com/polifonia-project/music-meta-ontology)