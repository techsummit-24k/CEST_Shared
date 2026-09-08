from neo4j import GraphDatabase
from config import (
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD,
    NEO4J_DATABASE,
)


class Neo4jReadClient:
    def __init__(self) -> None:
        self.driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
        )

    def close(self) -> None:
        self.driver.close()

    def query(self, cypher: str) -> list[dict]:
        with self.driver.session(database=NEO4J_DATABASE) as session:
            result = session.run(cypher)
            return [record.data() for record in result]