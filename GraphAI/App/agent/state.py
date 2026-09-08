from typing import TypedDict, Any


class AgentState(TypedDict, total=False):
    question: str
    safe: bool
    refusal_reason: str
    cypher: str
    cypher_error: str
    records: list[dict[str, Any]]
    answer: str
    sources: list[str]
    limitation: str