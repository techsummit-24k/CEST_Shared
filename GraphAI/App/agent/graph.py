
import time
import re
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_random_exponential

from config import (
    AGENT_MAX_RETRIES,
    AGENT_MAX_ROWS,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    OLLAMA_BASE_URL,
    OLLAMA_MAX_RETRIES,
    OLLAMA_MODEL,
    USE_OLLAMA,
)
from prompts import (
    ANSWER_SYSTEM_PROMPT,
    CYPHER_SYSTEM_PROMPT,
    OLLAMA_CYPHER_REPAIR_PROMPT,
    OLLAMA_CYPHER_SYSTEM_PROMPT,
)
from state import AgentState
from tools.cypher_validator import validate_read_only_cypher
from tools.neo4j_read_tool import Neo4jReadClient

ollama_llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0,
)
gemini_llm = (
    ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        temperature=0,
        google_api_key=GEMINI_API_KEY,
    )
    if GEMINI_API_KEY and not USE_OLLAMA
    else None
)
active_provider = "Ollama" if USE_OLLAMA else "Gemini"
provider_status_callback = None
neo4j_client = Neo4jReadClient()


def response_text(response) -> str:
    content = response.content
    if isinstance(content, str):
        return content.strip()
    return "".join(
        part.get("text", "") if isinstance(part, dict) else str(part)
        for part in content
    ).strip()


@retry(
    wait=wait_random_exponential(min=2, max=10),
    stop=stop_after_attempt(AGENT_MAX_RETRIES),
    retry=retry_if_exception_type(Exception),
    reraise=True,
)
def call_gemini(messages):
    if gemini_llm is None:
        raise RuntimeError("Gemini is not configured with a GEMINI_API_KEY")
    return gemini_llm.invoke(messages)


def invoke_model(messages, ollama_messages=None):
    global active_provider

    time.sleep(4)  # Rate limit to avoid 429 errors from Gemini API
    if USE_OLLAMA:
        set_active_provider("Ollama (forced)")
        return ollama_llm.invoke(ollama_messages or messages)
    try:
        set_active_provider("Gemini (trying...)")
        response = call_gemini(messages)
        set_active_provider("Gemini")
        return response
    except Exception as error:
        error_type = type(error).__name__
        set_active_provider(f"Ollama (Gemini fallback: {error_type})")
        return ollama_llm.invoke(ollama_messages or messages)


def set_active_provider(provider: str) -> None:
    global active_provider
    active_provider = provider
    if provider_status_callback is not None:
        provider_status_callback(provider)


def set_provider_status_callback(callback) -> None:
    global provider_status_callback
    provider_status_callback = callback


def get_active_provider() -> str:
    return active_provider


def triage_ollama_cypher(cypher: str, max_rows: int) -> str:
    """Reject common local-model mistakes before a query reaches Neo4j."""
    cleaned = cypher.strip()
    if cleaned.startswith("```") and cleaned.endswith("```"):
        cleaned = cleaned.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    if "```" in cleaned:
        raise ValueError("Remove markdown code fences from the Cypher output.")
    if re.search(r"\{[^{}:]+\}", cleaned):
        raise ValueError("Replace unresolved Cypher parameters with literal values.")

    identifier = r"[A-Za-z_]\w*"
    aliases = set(re.findall(rf"\(\s*({identifier})\s*:\s*\w+", cleaned))
    aliases.update(re.findall(rf"\[\s*({identifier})\s*:\s*\w+", cleaned))
    referenced = set(re.findall(rf"\b({identifier})\s*\.", cleaned))
    undefined = referenced - aliases - {"labels", "type"}
    if undefined:
        raise ValueError(f"Undefined Cypher aliases: {', '.join(sorted(undefined))}.")

    return validate_read_only_cypher(cleaned, max_rows=max_rows)


def generate_ollama_cypher(question: str, initial_cypher: str) -> str:
    candidate = initial_cypher
    attempts = max(1, OLLAMA_MAX_RETRIES)
    for attempt in range(attempts):
        try:
            return triage_ollama_cypher(candidate, AGENT_MAX_ROWS)
        except ValueError as error:
            if attempt == attempts - 1:
                raise
            response = ollama_llm.invoke([
                ("system", OLLAMA_CYPHER_REPAIR_PROMPT),
                (
                    "user",
                    f"Question:\n{question}\n\n"
                    f"Candidate query:\n{candidate}\n\n"
                    f"Triage error:\n{error}",
                ),
            ])
            candidate = response_text(response)
    raise RuntimeError("Ollama Cypher generation failed.")


def safety_check(state: AgentState) -> AgentState:
    question = state["question"].lower()
    blocked_phrases = [
        "what should i take",
        "what medicine should",
        "what dose",
        "dosage",
        "diagnose",
        "diagnosis",
        "prescribe",
        "patient-specific",
        "emergency",
        "symptoms i have",
        "symptoms my",
    ]

    if any(phrase in question for phrase in blocked_phrases):
        return {
            **state,
            "safe": False,
            "refusal_reason": (
                "I cannot provide diagnosis, medication, dosage, or "
                "patient-specific treatment advice. I can help explore "
                "educational biomedical research relationships in this graph."
            ),
        }

    return {**state, "safe": True}


def route_after_safety(state: AgentState) -> str:
    return "generate_cypher" if state.get("safe") else "refuse"


def generate_cypher(state: AgentState) -> AgentState:
    gemini_messages = [
        ("system", CYPHER_SYSTEM_PROMPT),
        ("user", state["question"]),
    ]
    ollama_messages = [
        ("system", OLLAMA_CYPHER_SYSTEM_PROMPT),
        ("user", state["question"]),
    ]
    response = invoke_model(gemini_messages, ollama_messages)

    cypher = response_text(response)

    if cypher == "REFUSE_MEDICAL_ADVICE":
        return {
            **state,
            "safe": False,
            "refusal_reason": (
                "I cannot provide medical advice. I can help query the "
                "workshop graph for research-oriented evidence paths."
            ),
        }

    if active_provider.startswith("Ollama"):
        cypher = generate_ollama_cypher(state["question"], cypher)

    return {**state, "cypher": cypher}


def route_after_cypher(state: AgentState) -> str:
    return "execute_query" if state.get("safe") else "refuse"


def execute_query(state: AgentState) -> AgentState:
    try:
        safe_cypher = validate_read_only_cypher(
            state["cypher"],
            max_rows=AGENT_MAX_ROWS,
        )
        records = neo4j_client.query(safe_cypher)
        return {
            **state,
            "cypher": safe_cypher,
            "records": records,
            "cypher_error": "",
        }
    except Exception as exc:
        return {
            **state,
            "records": [],
            "cypher_error": str(exc),
        }


def answer_from_evidence(state: AgentState) -> AgentState:
    if state.get("cypher_error"):
        return {
            **state,
            "answer": (
                "I could not safely execute a graph query for that question. "
                "Try naming a disease, drug, gene, protein, or relationship "
                "that exists in the workshop dataset."
            ),
            "sources": [],
            "limitation": "No graph evidence was retrieved.",
        }

    if not state.get("records"):
        return {
            **state,
            "answer": (
                "The graph returned no matching records for this question. "
                "Try a more specific entity name or inspect the available "
                "labels and properties in Neo4j Browser."
            ),
            "sources": [],
            "limitation": (
                "No result does not mean the relationship is absent in "
                "biomedical reality; it may be absent from this curated dataset."
            ),
        }

    response = invoke_model([
        ("system", ANSWER_SYSTEM_PROMPT),
        (
            "user",
            f"Question:\n{state['question']}\n\n"
            f"Cypher used:\n{state['cypher']}\n\n"
            f"Graph records:\n{state['records']}",
        ),
    ])

    sources = sorted({
        str(value)
        for record in state["records"]
        for key, value in record.items()
        if "source" in key.lower() and value
    })

    return {
        **state,
        "answer": response_text(response),
        "sources": sources,
        "limitation": (
            "This response is based on a curated educational graph. "
            "Graph associations and prediction scores are research hypotheses, "
            "not causal proof, clinical validation, or medical advice."
        ),
    }


def refuse(state: AgentState) -> AgentState:
    return {
        **state,
        "answer": state.get(
            "refusal_reason",
            "I cannot assist with that medical request.",
        ),
        "sources": [],
        "limitation": (
            "This workshop agent is limited to public-data, "
            "research-oriented graph exploration."
        ),
    }



builder = StateGraph(AgentState)

builder.add_node("safety_check", safety_check)
builder.add_node("generate_cypher", generate_cypher)
builder.add_node("execute_query", execute_query)
builder.add_node("answer_from_evidence", answer_from_evidence)
builder.add_node("refuse", refuse)

builder.set_entry_point("safety_check")

builder.add_conditional_edges(
    "safety_check",
    route_after_safety,
    {
        "generate_cypher": "generate_cypher",
        "refuse": "refuse",
    },
)

builder.add_conditional_edges(
    "generate_cypher",
    route_after_cypher,
    {
        "execute_query": "execute_query",
        "refuse": "refuse",
    },
)

builder.add_edge("execute_query", "answer_from_evidence")
builder.add_edge("answer_from_evidence", END)
builder.add_edge("refuse", END)

clinical_research_agent = builder.compile()