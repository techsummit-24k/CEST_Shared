CALL gds.graph.exists('clinicalGraph')
YIELD exists
RETURN exists;

CALL gds.graph.drop('clinicalGraph', false)
YIELD graphName
RETURN graphName;

CALL gds.graph.project(
  'clinicalGraph',
  ['Drug', 'Protein', 'Gene', 'Disease', 'Pathway'],
  {
    TARGETS: {orientation: 'UNDIRECTED'},
    ENCODED_BY: {orientation: 'UNDIRECTED'},
    ASSOCIATED_WITH: {
      orientation: 'UNDIRECTED',
      properties: 'evidence_score'
    },
    TREATS: {orientation: 'UNDIRECTED'},
    PARTICIPATES_IN: {orientation: 'UNDIRECTED'}
  }
)
YIELD graphName, nodeCount, relationshipCount
RETURN graphName, nodeCount, relationshipCount;



// Exercise 1: Who is structurally influential?
CALL gds.pageRank.stream('clinicalGraph')
YIELD nodeId, score
WITH gds.util.asNode(nodeId) AS node, score
RETURN coalesce(node.name, node.symbol, node.id) AS entity,
       labels(node) AS entity_type,
       round(score, 4) AS pagerank
ORDER BY pagerank DESC
LIMIT 20;


// Exercise 2: Identify graph communities.
CALL gds.louvain.stream('clinicalGraph')
YIELD nodeId, communityId
WITH gds.util.asNode(nodeId) AS node, communityId
RETURN communityId,
       collect(coalesce(node.name, node.symbol, node.id))[0..10] AS sample_entities,
       count(*) AS community_size
ORDER BY community_size DESC;


#### Disease Similarity
Data to be set

MATCH (d1:Disease)<-[:ASSOCIATED_WITH]-(g:Gene)-[:ASSOCIATED_WITH]->(d2:Disease)
WHERE d1.id < d2.id
RETURN
  d1.name AS disease_1,
  d2.name AS disease_2,
  collect(DISTINCT g.symbol) AS shared_genes,
  count(DISTINCT g) AS shared_gene_count
ORDER BY shared_gene_count DESC, disease_1, disease_2;


CALL gds.graph.drop('diseaseSimilarityGraph', false)
YIELD graphName
RETURN graphName;

CALL gds.graph.project(
  'diseaseSimilarityGraph',
  ['Disease', 'Gene'],
  {
    ASSOCIATED_WITH: {
      orientation: 'REVERSE'
    }
  }
)
YIELD graphName, nodeCount, relationshipCount
RETURN graphName, nodeCount, relationshipCount;




// Exercise 3: Find disease similarity through shared neighborhood.
CALL gds.nodeSimilarity.stream(
  'diseaseSimilarityGraph',
  {
    nodeLabels: ['Disease'],
    relationshipTypes: ['ASSOCIATED_WITH'],
    similarityCutoff: 0.1
  }
)
YIELD node1, node2, similarity
RETURN gds.util.asNode(node1).name AS disease_1,
       gds.util.asNode(node2).name AS disease_2,
       round(similarity, 3) AS similarity
ORDER BY similarity DESC
LIMIT 20;



