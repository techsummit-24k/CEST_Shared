from typing import List, TypedDict
# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langgraph.graph import END, StateGraph
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# --- LINK TO THE SHARED DB ---
OLLAMA_BASE_URL="http://localhost:11434"
embeddings = OllamaEmbeddings(model="nomic-embed-text",base_url=OLLAMA_BASE_URL)
db = Chroma(persist_directory="./agent_db", embedding_function=embeddings)
retriever = db.as_retriever()
# llm = ChatOllama(model="deepseek-r1:8b", temperature=0,base_url=OLLAMA_BASE_URL)
llm = ChatOllama(model="llama3.2:latest", temperature=0,base_url=OLLAMA_BASE_URL)

# --- Pydantinc Class to force Structural Output--- 
class GradeDocuments(BaseModel):
    binary_score: str = Field(description="Documents are relevant to the question, 'yes' or 'no'")

# --- AGENT STATE ---
class GraphState(TypedDict):
    question: str
    documents: List[str] # This holds the snippets we find
    generation: str

# --- NODES (The Logic) ---

def retrieve(state):
    # Search the DB for the top 3 snippets (Documents)
    print(f"{state["question"]}")
    docs = retriever.invoke(state["question"])
    return {"documents": docs}

def grade_documents(state):
    print("--- CHECKING DOCUMENT RELEVANCE ---")
    
    # Set up the Grader
    structured_llm_grader = llm.with_structured_output(GradeDocuments)
    documents = state["documents"]
    question = state["question"]
    
    system = """You are a grader assessing relevance of a retrieved document to a user question. 
    If the document contains keywords or semantic meaning related to the user question, grade it as relevant. 
    Give a binary score 'yes' or 'no' to indicate whether the document is relevant to the question."""
    
    grade_prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
    ])

    grader_chain = grade_prompt | structured_llm_grader
    
    valid_docs=[]
    
    #Loop through EVERY document retrieved
    for d in documents:
        score = grader_chain.invoke({
            "question": question, 
            "document": d.page_content
        })
        
        if score.binary_score == "yes":
            print("  - Found a relevant snippet!")
            valid_docs.append(d)
        else:
            print("  - Snippet irrelevant, skipping.")
    
    # score = grader_chain.invoke({"question": state["question"], "document": doc_txt})
    
    # if score.binary_score == "yes":
    if valid_docs:
        return {"documents": valid_docs, "generation": "generate"}
    else:
        # Nothing was useful
        print("--- NO RELEVANT DOCS FOUND. TRIGGERING REWRITE ---")
        return {"generation": "transform_query"}

def transform_query(state):
    print("--- ACTION: CONTEXT-AWARE REWRITE ---")
    question = state["question"]
    bad_docs = state["documents"] # The snippets that weren't relevant
    
    # We show the LLM what "kind" of data is in the DB to help it steer
    sample_context = "\n".join([d.page_content[:200] for d in bad_docs])

    system_prompt = """You are a search optimizer. You previously searched for a question but found irrelevant results.
    Based on the 'Irrelevant Snippets' provided, understand the vocabulary and structure of the document, 
    then rewrite the user's question to better navigate this specific database."""

    user_content = f"""
    Original Question: {question}
    
    Irrelevant Snippets Found:
    {sample_context}
    
    Instructions: Rewrite the question to avoid these irrelevant topics and target the actual intent. 
    Only output the new question text.
    """
    
    better_q = llm.invoke([
        ("system", system_prompt),
        ("human", user_content)
    ])
    
    return {"question": better_q.content, "documents": []} # Clear docs for the next search

def generate(state):
    print("--- STEP: GENERATING ANSWER ---")
    question = state["question"]
    documents = state["documents"] # These are the snippets from the DB
    
    # 1. Combine all snippet text into one big string
    context = "\n\n".join([doc.page_content for doc in documents])
    
    # 2. Create the "Source-Based" prompt
    prompt = f"""
    You are an assistant. Use ONLY the following context to answer the question. 
    If the answer isn't in the context, say you don't know.
    
    CONTEXT:
    {context}
    
    QUESTION: 
    {question}
    
    ANSWER:
    """
    
    # 3. Ask the Local LLM (Ollama)
    response = llm.invoke(prompt)
    
    return {"generation": response.content}

# --- THE GRAPH (The Routing) ---
workflow = StateGraph(GraphState)
workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_documents", grade_documents)
workflow.add_node("transform_query", transform_query)
workflow.add_node("generate", generate)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "grade_documents")

# This is the "Brain" choosing the path
workflow.add_conditional_edges(
    "grade_documents",
    lambda x: x["generation"], # Path depends on the grade result
    {
        "transform_query": "transform_query",
        "generate": "generate"
    }
)
workflow.add_edge("transform_query", "retrieve") # Loop back to search again
workflow.add_edge("generate", END)

app = workflow.compile()


if __name__ == "__main__":
    print("\n--- Agentic RAG Live ---")
    query = input("Place your query here: ")
    # query  = "Has he worked in Cognizant?"
    
    # Run the graph
    value = app.invoke({"question": query})
    # print(value.keys())
    
    # Access the result (using single quotes inside the f-string)
    final_result = value.get("generation", "Nothing returned")
    print(f"\nFinal Answer: {final_result}")

