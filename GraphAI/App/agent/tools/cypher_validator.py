import re

FORBIDDEN_TERMS = [
    "CREATE", "MERGE", "DELETE", "DETACH", "SET", "REMOVE", "DROP",
    "LOAD CSV", "CALL", "APOC", "DBMS", "FOREACH", "UNWIND"
]

ALLOWED_START = ("MATCH", "OPTIONAL MATCH", "WITH")

def validate_read_only_cypher(cypher: str, max_rows: int = 30) -> str:
    if not cypher or not cypher.strip():
        raise ValueError("Empty Cypher query.")

    query = cypher.strip().rstrip(";")
    upper = query.upper()

    if not upper.startswith(ALLOWED_START):
        raise ValueError("Only read-only MATCH/OPTIONAL MATCH/WITH queries are allowed.")

    for term in FORBIDDEN_TERMS:
        if re.search(rf"\b{re.escape(term)}\b", upper):
            raise ValueError(f"Forbidden Cypher operation: {term}")

    if "RETURN" not in upper:
        raise ValueError("A read-only query must return results.")

    if "LIMIT" not in upper:
        query = f"{query}\nLIMIT {max_rows}"

    limit_match = re.search(r"\bLIMIT\s+(\d+)\b", query, flags=re.IGNORECASE)
    if limit_match and int(limit_match.group(1)) > max_rows:
        query = re.sub(
            r"\bLIMIT\s+\d+\b",
            f"LIMIT {max_rows}",
            query,
            flags=re.IGNORECASE,
        )

    return query