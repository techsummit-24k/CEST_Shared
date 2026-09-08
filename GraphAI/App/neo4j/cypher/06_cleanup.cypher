CALL gds.graph.exists('clinicalGraph')
YIELD exists
WITH exists
WHERE exists
CALL gds.graph.drop('clinicalGraph')
YIELD graphName
RETURN graphName;

MATCH (n)
DETACH DELETE n;

SHOW CONSTRAINTS;

