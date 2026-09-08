Drug → Protein → Gene → Disease


### Link Predictions

MATCH (drug:Drug)-[:TARGETS]->(protein:Protein)-[:ENCODED_BY]->(gene:Gene)
MATCH (gene)-[assoc:ASSOCIATED_WITH]->(disease:Disease)
WHERE NOT (drug)-[:TREATS]->(disease)
WITH drug, disease,
     collect(DISTINCT gene.symbol) AS supporting_genes,
     collect(DISTINCT protein.name) AS supporting_proteins,
     count(DISTINCT gene) AS gene_support_count,
     avg(coalesce(assoc.evidence_score, 0.0)) AS mean_gene_disease_evidence,
     max(coalesce(assoc.evidence_score, 0.0)) AS max_gene_disease_evidence
RETURN
  drug.name AS candidate_drug,
  disease.name AS candidate_disease,
  gene_support_count,
  round(mean_gene_disease_evidence, 3) AS mean_evidence_score,
  round(max_gene_disease_evidence, 3) AS maximum_evidence_score,
  supporting_genes,
  supporting_proteins,
  round(
    gene_support_count * mean_gene_disease_evidence,
    3
  ) AS candidate_score
ORDER BY candidate_score DESC,
         gene_support_count DESC,
         mean_evidence_score DESC
LIMIT 20;

### Supporting paths
### first add the param values of interest

:param candidate_drug => "Example Compound 01";
:param candidate_disease => "Type 2 Diabetes Mellitus";

MATCH path =
  (drug:Drug {name: $candidate_drug})-[:TARGETS]->(protein:Protein)
  -[:ENCODED_BY]->(gene:Gene)
  -[assoc:ASSOCIATED_WITH]->(disease:Disease {name: $candidate_disease})
RETURN
  path,
  gene.symbol AS supporting_gene,
  protein.name AS supporting_protein,
  assoc.evidence_score AS evidence_score,
  assoc.evidence_type AS evidence_type,
  assoc.source AS source
ORDER BY evidence_score DESC;


### Visualize a Prediction View

MATCH (drug:Drug)-[:TARGETS]->(:Protein)-[:ENCODED_BY]->(gene:Gene)
MATCH (gene)-[assoc:ASSOCIATED_WITH]->(disease:Disease)
WHERE NOT (drug)-[:TREATS]->(disease)
WITH drug, disease,
     count(DISTINCT gene) AS gene_support_count,
     avg(coalesce(assoc.evidence_score, 0.0)) AS mean_evidence_score
WITH drug, disease, gene_support_count, mean_evidence_score,
     gene_support_count * mean_evidence_score AS candidate_score
WHERE candidate_score >= 0.5
MERGE (drug)-[r:PREDICTED_TREATS]->(disease)
SET r.score = round(candidate_score, 3),
    r.supporting_gene_count = gene_support_count,
    r.mean_evidence_score = round(mean_evidence_score, 3),
    r.method = "Drug-Protein-Gene-Disease topology",
    r.status = "research hypothesis only",
    r.created_for = "workshop demonstration";


  ### and Visualize only the Candidate links

  MATCH path =
  (drug:Drug)-[prediction:PREDICTED_TREATS]->(disease:Disease)
RETURN path
ORDER BY prediction.score DESC
LIMIT 20;


  ### Delete the Temporary relationshipTypes

  MATCH ()-[r:PREDICTED_TREATS]->()
DELETE r;
