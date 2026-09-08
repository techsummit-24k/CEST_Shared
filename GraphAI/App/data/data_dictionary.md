### Graph

(:Drug)-[:TARGETS]->(:Protein)
(:Protein)-[:ENCODED_BY]->(:Gene)
(:Gene)-[:ASSOCIATED_WITH]->(:Disease)
(:Drug)-[:TREATS]->(:Disease)
(:Gene)-[:PARTICIPATES_IN]->(:Pathway)
(:Publication)-[:SUPPORTS]->(:Drug|:Gene|:Disease)

### Nodes

| Node label  | ID column      | Essential properties                      |
| ----------- | -------------- | ----------------------------------------- |
| Drug        | drug_id        | name, approval_status, drug_class, source |
| Disease     | disease_id     | name, therapeutic_area, source            |
| Gene        | gene_id        | symbol, name, source                      |
| Protein     | protein_id     | name, uniprot_id, source                  |
| Pathway     | pathway_id     | name, source                              |
| Publication | publication_id | title, year, pmid, source                 |

### Relationship Types

| Relationship    | From        | To                  | Useful properties                       |
| --------------- | ----------- | ------------------- | --------------------------------------- |
| TARGETS         | Drug        | Protein             | action, evidence_score, source          |
| ENCODED_BY      | Protein     | Gene                | source                                  |
| ASSOCIATED_WITH | Gene        | Disease             | evidence_score, evidence_type, source   |
| TREATS          | Drug        | Disease             | approval_status, evidence_score, source |
| PARTICIPATES_IN | Gene        | Pathway             | source                                  |
| SUPPORTS        | Publication | Any evidence entity | relation_type, source, confidence       |


### Required Provenance Fields

source
evidence_score
evidence_type