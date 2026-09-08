MATCH (n)
RETURN labels(n) AS node_type, count(*) AS count
ORDER BY count DESC;

MATCH ()-[r]->()
RETURN type(r) AS relationship_type, count(*) AS count
ORDER BY count DESC;

MATCH (drug:Drug)
WHERE NOT (drug)-[:TARGETS]->()
RETURN drug.id AS drug_without_target, drug.name
LIMIT 20;

MATCH (gene:Gene)
WHERE NOT (gene)-[:ASSOCIATED_WITH]->()
RETURN gene.id AS gene_without_disease_link, gene.symbol
LIMIT 20;

MATCH ()-[r]->()
WHERE r.source IS NULL
RETURN type(r) AS relationship_type, count(*) AS missing_source_count;

MATCH path =
  (:Drug)-[:TARGETS]->(:Protein)-[:ENCODED_BY]->(:Gene)
  -[:ASSOCIATED_WITH]->(:Disease)
RETURN path
LIMIT 25;