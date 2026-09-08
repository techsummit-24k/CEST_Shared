import os
from pathlib import Path

from dotenv import load_dotenv

AGENT_DIR = Path(__file__).resolve().parent
load_dotenv(AGENT_DIR / ".env")
if not (AGENT_DIR / ".env").exists():
	load_dotenv(AGENT_DIR / ".env.example")

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "clinicalkg2026")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
USE_OLLAMA = os.getenv("USE_OLLAMA", "false").strip().lower() in {"1", "true", "yes", "on"}
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
AGENT_MAX_ROWS = int(os.getenv("AGENT_MAX_ROWS", "30"))
AGENT_MAX_RETRIES = int(os.getenv("AGENT_MAX_RETRIES", "1"))
OLLAMA_MAX_RETRIES = int(os.getenv("OLLAMA_MAX_RETRIES", "2"))