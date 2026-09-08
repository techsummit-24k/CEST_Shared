Streamlit user interface
        ↓
LangGraph state machine
        ↓
Question classification / safety check
        ↓
Cypher generation via LLM
        ↓
Cypher validator and read-only allowlist
        ↓
Neo4j Python driver over Bolt
bolt://localhost:7687
        ↓
Structured graph records
        ↓
Evidence formatter
        ↓
Grounded research response:
answer + Cypher + sources + limitations


How to run:

In the App/agent folder run

#### Set up the Virtual Environment

```bash
python -m venv .venv

. ./.venv/scripts/activate

```

#### Install the dependencies

```bash
pip install -r requirements.txt
```

#### Run the stereamlit app

```bash
streamlit run app.py
```

