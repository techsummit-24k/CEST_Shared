# HandsOn Knowledge Graphs and Graph AI for Biomedical Research

## Learning goals

By the end of this workshop, I can:
- Explain why connected biomedical data suits graphs
- Run Neo4j with Docker
- Build a Drug–Gene–Disease graph
- Write and adapt Cypher queries
- Apply basic graph analytics
- Interpret a graph-based candidate link responsibly
- Ask an AI agent a research-grade graph question

## Lab 0 — Environment check

1. Start Docker Desktop
2. In the workshop folder, run:
   docker compose up -d
3. Open http://localhost:7474
4. Login to Neo4j
5. Run:
   RETURN "Ready for Clinical Knowledge Graph Lab" AS status;

[Checkpoint: Screenshot your successful result.]

## Lab 1 — My graph schema

Draw or annotate this:

Drug → TARGETS → Protein → ENCODED_BY → Gene
Gene → ASSOCIATED_WITH → Disease
Drug → TREATS → Disease

Questions:
1. Which relationships require an evidence score?
2. Which relationships require a source?
3. What additional entity would improve this graph?
   Pathway / Publication / Side effect / Clinical trial

## Lab 2 — Import and validate

Run:
- 00_setup.cypher
- 01_import_graph.cypher
- 02_validate_graph.cypher

Record:
- Number of Drug nodes:
- Number of Disease nodes:
- Number of Gene nodes:
- Number of TARGETS relationships:
- Does every relationship have a source?

## Lab 3 — Cypher investigation

Choose one disease:
[                    ]

Write your research question:
[                    ]

Paste or write your Cypher query:
[                    ]

What evidence path did you find?
[Drug → Protein → Gene → Disease]

Evidence source(s):
[                    ]

## Lab 4 — Graph AI

Before running PageRank, predict the most influential node type:
[Drug / Protein / Gene / Disease]

Result:
[                    ]

One interpretation:
[                    ]

One limitation:
[                    ]

## Lab 5 — Link prediction

Candidate drug:
[                    ]

Candidate disease:
[                    ]

Supporting genes:
[                    ]

Prediction / network score:
[                    ]

Why is this only a hypothesis and not a treatment claim?
[                    ]

## Lab 6 — AI research agent

Question asked:
[                    ]

Cypher generated:
[                    ]

Did the agent show sources and limitations?
[Yes / No]

How would you improve the question?
[                    ]

## Team challenge

Present:
1. Disease investigated
2. One candidate research hypothesis
3. Evidence path
4. Source and score
5. Limitation
6. Next validation step