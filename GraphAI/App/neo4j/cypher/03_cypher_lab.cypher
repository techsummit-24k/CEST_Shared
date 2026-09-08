// Exercise 1: List all diseases in the graph.
MATCH (d:Disease)
RETURN d.name AS disease, d.therapeutic_area AS area
ORDER BY disease;

// Exercise 2: Find approved drugs that treat Type 2 Diabetes Mellitus.
MATCH (drug:Drug)-[r:TREATS]->(disease:Disease)
WHERE disease.name = "Type 2 Diabetes Mellitus"
RETURN drug.name AS drug,
       drug.drug_class AS class,
       r.approval_status AS status,
       r.source AS evidence_source;


// Exercise 3: Find genes associated with Breast Cancer.
MATCH (gene:Gene)-[r:ASSOCIATED_WITH]->(disease:Disease)
WHERE disease.name = "Breast Cancer"
RETURN gene.symbol AS gene,
       gene.name AS gene_name,
       r.evidence_score AS evidence_score,
       r.evidence_type AS evidence_type
ORDER BY evidence_score DESC;


// Exercise 4: Trace a mechanism path for Imatinib.
MATCH path =
  (drug:Drug {name: "Imatinib"})-[:TARGETS]->(:Protein)
  -[:ENCODED_BY]->(:Gene)-[:ASSOCIATED_WITH]->(:Disease)
RETURN path;


// Exercise 5: Find genes and pathways connected to a disease.
MATCH (gene:Gene)-[:ASSOCIATED_WITH]->(disease:Disease)
WHERE disease.name = "Type 2 Diabetes Mellitus"
OPTIONAL MATCH (gene)-[:PARTICIPATES_IN]->(pathway:Pathway)
RETURN gene.symbol AS gene,
       collect(DISTINCT pathway.name) AS pathways;


// Exercise 6: Candidate research links.
// These are not validated treatments and must be presented as hypotheses.
MATCH (drug:Drug)-[:TARGETS]->(:Protein)-[:ENCODED_BY]->(gene:Gene)
MATCH (gene)-[assoc:ASSOCIATED_WITH]->(disease:Disease)
WHERE NOT (drug)-[:TREATS]->(disease)
RETURN drug.name AS candidate_drug,
       disease.name AS candidate_disease,
       count(DISTINCT gene) AS supporting_gene_count,
       round(avg(assoc.evidence_score), 3) AS mean_evidence_score,
       collect(DISTINCT assoc.source) AS sources
ORDER BY supporting_gene_count DESC, mean_evidence_score DESC
LIMIT 20;


// Exercise 7: Explain one candidate with a visible evidence path.
MATCH path =
  (drug:Drug)-[:TARGETS]->(:Protein)-[:ENCODED_BY]->(:Gene)
  -[assoc:ASSOCIATED_WITH]->(disease:Disease)
WHERE drug.name = $drug_name
  AND disease.name = $disease_name
RETURN path,
       assoc.evidence_score AS evidence_score,
       assoc.source AS source
LIMIT 20;


