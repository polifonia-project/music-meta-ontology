<p align="left">
<img src="website/static/img/musicmeta_logo.png" width="140">
</p>

# Music Meta

A **rich** and **flexible** semantic model to describe **music metadata** related to artists, compositions, performances, recordings, broadcasts, and links. Music Meta provides an **abstraction** layer to represent (Western) music metadata across different genres and periods, for various stakeholders and music datasets. The ontology is thus designed to be specialised to the specific contexts of application (see some examples below) and is part of the Polifonia Ontology Network.

**How?** We follow eXtreme Design methodologies and best practices for data engineering [1], to reflect the perspectives and the requirements of various stakeholders into the design of the model, while leveraging ontology design patterns and accounting for provenance at different levels (claims, links). We provide a first evaluation of the model, alignments to other schema (Music Ontology, DOREMUS, Wikidata), and support for data transformation.

**Why another ontology for music metadata?** The interoperability of metadata is an essential requirement for the integration of music datasets, which is curently hampered by the specificity of existent ontologies. The semantic description of music metadata is indeed a key requirement for the creation of music datasets that can be aligned, integrated, and accessed for information retrieval and knowledge discovery. It is nonetheless an open challenge due to the complexity of musical concepts arising from different genres, styles, and time periods – hence requiring a lingua franca to accommodate various stakeholders (music librarians, musicologists, music analysts, cataloguers, data engineers, etc.).


## Competency questions addressed

- Which is the composer of a musical piece?
  -  Is the composer of a musical piece known?
-  Which are the members of a music ensemble?
-  Which role a music artist played within a music ensemble?
-  In which time interval has a music artist been a member of a music ensemble?
-  Where was a music ensemble formed?
-  Which award was a music artist nominated for?
-  Which award was received by a music artist?
-  Which music artists has a music artist been influenced by?
-  Which music artist has a music artist collaborated with?
-  Which is the start date of the activity of a music artist?
-  Which is the end date of the activity of a music artist?
-  Which is the name of a music artist?
-  Which is the alias of a music artist?
-  Which is the language of the name/alias of a music artist?
-  Which music dataset has a music algorithm been trained on?
-  Which is the process that led to the creation of a musical piece?
-  In which time interval did the creation process took place?
-  Where did the creation process took place?
-  Which are the creative actions composing the creation process of a musical piece?
-  Which task was executed by a creative action?
-  Which are the parts of a musical piece?
-  Which collection is a musical piece member of?
-  Where was a musical piece performed?
-  When was a musical piece performed?
- Which music artists took part to a musical performance?
- Which is the recording process that recorded a musical performance?
- Which is the recording produced by a recording process?
  
  
## Examples of SPARQL queries addressed
- Which are the members of a music ensemble?
```
PREFIX mm: <https://w3id.org/polifonia/ontology/music-meta/>
PREFIX core: <https://w3id.org/polifonia/ontology/core/>
SELECT DISTINCT ?musicEnsembleMember
WHERE { ?musicEnsembleMember core:isMemberOf ?musicEnsemble .
?musicEnsemble rdf:type mm:MusicEnsemble .
}
```

- Which role a music artist played within a music ensemble?
```
PREFIX mm: <https://w3id.org/polifonia/ontology/music-meta/>
PREFIX core: <https://w3id.org/polifonia/ontology/core/>
SELECT DISTINCT ?musicEnsembleMember ?musicEnsembleMemberRole
WHERE { ?musicEnsembleMember mm:isMemberOfMusicEnsembleInvolvedIn ?musicEnsembleMembership .
?musicEnsembleMembership rdf:type mm:MusicEnsembleMembership ;
core:involvesRole ?musicEnsembleMemberRole .
}
```

## References

[1] E. Blomqvist, K. Hammar, and V. Presutti, “Engineering Ontologies with Patterns-The eXtreme Design Methodology.” Ontology Engineering with Ontology Design Patterns, no. 25, 2016.

