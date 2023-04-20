# Music Meta
Our flagship ontology to describe music metadata

## Competency questions addressed by this ontology module 

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
  
  
## Examples of SPARQL queries addressed by the module
- Which are the members of a music ensemble?
```
PREFIX mm: <https://w3id.org/polifonia/ontology/music-meta/>
SELECT DISTINCT ?musicEnsembleMember
WHERE { ?musicEnsembleMember mm:isMemberOf ?musicEnsemble .
?musicEnsemble rdf:type mm:MusicEnsemble .
}
```
