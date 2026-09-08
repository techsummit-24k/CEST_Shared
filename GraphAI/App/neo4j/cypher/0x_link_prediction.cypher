// Confirm the graph projection exists.
CALL gds.graph.list('clinicalGraph')
YIELD graphName, nodeCount, relationshipCount
RETURN graphName, nodeCount, relationshipCount;


// Rank potential Drug-Disease pairs using common-neighbor structure.
CALL gds.linkPrediction.commonNeighbors.stream(
  'clinicalGraph',
  {
    sourceNodeFilter: 'Drug',
    targetNodeFilter: 'Disease'
  }
)
YIELD node1, node2, score
WITH gds.util.asNode(node1) AS drug,
     gds.util.asNode(node2) AS disease,
     score
WHERE NOT (drug)-[:TREATS]->(disease)
RETURN drug.name AS candidate_drug,
       disease.name AS candidate_disease,
       score AS common_neighbors_score
ORDER BY common_neighbors_score DESC
LIMIT 20;
There is no procedure with the name `gds.linkPrediction.commonNeighbors.stream` registered for this database instance. Please ensure you've spelled the procedure name correctly and that the procedure is properly deployed.

// Add explanatory evidence paths for candidates.
// This is still a research-hypothesis query, not a medical conclusion.
MATCH (drug:Drug)-[:TARGETS]->(:Protein)-[:ENCODED_BY]->(gene:Gene)
MATCH (gene)-[assoc:ASSOCIATED_WITH]->(disease:Disease)
WHERE NOT (drug)-[:TREATS]->(disease)
RETURN drug.name AS candidate_drug,
       disease.name AS candidate_disease,
       count(DISTINCT gene) AS supporting_genes,
       round(avg(assoc.evidence_score), 3) AS mean_evidence_score,
       collect(DISTINCT gene.symbol)[0..8] AS supporting_gene_symbols,
       collect(DISTINCT assoc.source) AS evidence_sources
ORDER BY supporting_genes DESC, mean_evidence_score DESC
LIMIT 20;


