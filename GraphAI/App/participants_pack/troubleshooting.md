| Problem                              | Likely cause                                                                        | Fix                                                                                               |
| ------------------------------------ | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| docker command not found             | Docker Desktop is not installed or terminal restarted before installation completed | Install/start Docker Desktop, close and reopen terminal                                           |
| Docker engine not running            | Docker Desktop not started                                                          | Open Docker Desktop and wait until it shows Engine Running                                        |
| Port 7474 already in use             | Another Neo4j/container/app uses it                                                 | Stop old container with docker ps, or change host port to 7475:7474                               |
| Port 7687 already in use             | Existing Neo4j instance                                                             | Stop existing container or change to 7688:7687 and update NEO4J_URI                               |
| Browser cannot open Neo4j            | Container is still starting or failed                                               | Run docker compose ps then docker compose logs neo4j                                              |
| Neo4j login rejected                 | Wrong password or old volume retains a previous password                            | Run docker compose down -v, then docker compose up -d                                             |
| file:///drugs.csv not found          | CSV not placed in mounted folder                                                    | Confirm files are in data/curated/, then restart container                                        |
| GDS procedure missing                | Plugin did not download/install                                                     | Check logs, internet access, then recreate with docker compose down -v and docker compose up -d   |
| Out of memory                        | Laptop has low available RAM                                                        | Quit browsers/IDEs, set heap/page cache to 512M, pair with another learner, or use cloud fallback |
| Agent cannot connect                 | Neo4j container not running or incorrect Bolt URI                                   | Check bolt://localhost:7687, credentials, and docker compose ps                                   |
| Agent returns forbidden Cypher error | Agent generated a write/admin query                                                 | Rephrase as a research lookup; validator correctly blocks unsafe query                            |
| Agent says no result                 | Entity name differs from graph dataset                                              | Query MATCH (n) RETURN labels(n), n.name, n.symbol LIMIT 30 to inspect available values           |
| Agent produces a medical answer      | Safety prompt/validator problem                                                     | Stop demo, use the refusal path, review prompts; never continue with patient-specific queries     |



### Quick Diagnostics

docker compose ps

docker compose logs neo4j --tail=100

docker compose down -v
docker compose up -d

RETURN "Neo4j connection confirmed" AS status;

CALL gds.version()
YIELD version
RETURN version;


### Run Order

| Session point                  | File / tool                                 |
| ------------------------------ | ------------------------------------------- |
| Participant pre-check          | participant-pack/setup-guide.md             |
| Start Neo4j                    | docker-compose.yml                          |
| Build database rules           | 00_setup.cypher                             |
| Load CSV graph                 | 01_import_graph.cypher                      |
| Check graph quality            | 02_validate_graph.cypher                    |
| Guided Cypher challenge        | 03_cypher_lab.cypher                        |
| Graph AI experience            | 04_gds_lab.cypher                           |
| Candidate-link activity        | 05_link_prediction.cypher                   |
| Natural-language “wow” demo    | agent/app.py                                |
| Team challenge review          | facilitator-pack/answer-key.md              |
| Reset for next rehearsal/batch | 06_cleanup.cypher or docker compose down -v |