# Expected workshop outputs

## After import

Expected node labels:
- Drug
- Disease
- Gene
- Protein
- Pathway
- Publication

Expected relationship types:
- TARGETS
- ENCODED_BY
- ASSOCIATED_WITH
- TREATS
- PARTICIPATES_IN

## Validation expectations

- Every Drug should have a unique `id`.
- Every Disease should have a unique `id`.
- No relationship should have a missing `source`.
- At least one visual path should exist:
  Drug → Protein → Gene → Disease.

## Cypher lab

- Metformin should return as an approved relationship for Type 2 Diabetes Mellitus.
- Imatinib should trace through ABL1 toward Chronic Myeloid Leukemia.
- Candidate queries may surface indirect Drug–Gene–Disease paths.
- A candidate must never be described as a treatment without an explicit `TREATS` relationship.

## GDS lab

- PageRank returns a ranked list of entities.
- Louvain returns communities.
- Node similarity may return no results in extremely small data fixtures.
  Use the full curated workshop data for this exercise.

## Prediction lab

- Common-neighbor scores rank structurally related, currently unlinked Drug–Disease pairs.
- Scores are hypothesis signals, not proof of efficacy or safety.