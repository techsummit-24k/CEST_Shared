import streamlit as st
from graph import (
    clinical_research_agent,
    get_active_provider,
    set_provider_status_callback,
)

st.set_page_config(
    page_title="Biomedical Research Graph Agent",
    page_icon="🧬",
    layout="wide",
)

st.title("Biomedical Research Graph Agent")
st.caption(
    "Educational Graph AI demonstration: evidence retrieval, "
    "Cypher transparency, and research-hypothesis exploration."
)
provider_status = st.sidebar.empty()
set_provider_status_callback(
    lambda provider: provider_status.info(
        f"Active model provider: **{provider}**"
    )
)
provider_status.info(f"Active model provider: **{get_active_provider()}**")

st.warning(
    "This tool is for public-data research exploration only. "
    "It does not provide diagnosis, medication, dosage, treatment, "
    "or patient-specific medical advice."
)

default_question = (
    "Which drugs target proteins connected to genes associated with "
    "Type 2 Diabetes Mellitus, excluding drugs already recorded as treating it?"
)

question = st.text_area(
    "Ask a graph-grounded biomedical research question",
    value=default_question,
    height=110,
)

if st.button("Ask the Research Agent", type="primary"):
    if not question.strip():
        st.error("Please enter a question.")
    else:
        with st.spinner("Generating safe Cypher and retrieving graph evidence..."):
            result = clinical_research_agent.invoke({"question": question})

        st.success(f"Response generated with **{get_active_provider()}**")
        st.subheader("Research response")
        st.write(result.get("answer", ""))

        st.subheader("Cypher used")
        st.code(result.get("cypher", "No query executed."), language="cypher")

        st.subheader("Retrieved graph records")
        records = result.get("records", [])
        if records:
            st.dataframe(records, use_container_width=True)
        else:
            st.info("No records returned.")

        st.subheader("Evidence sources")
        sources = result.get("sources", [])
        if sources:
            st.write(", ".join(sources))
        else:
            st.write("No source field was returned.")

        st.subheader("Limitation")
        st.info(result.get("limitation", "No limitation supplied."))