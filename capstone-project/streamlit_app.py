"""
Streamlit interface for the handbook RAG assistant.
Logs every Q&A + user feedback to SQLite for the monitoring dashboard.

Usage:
    STREAMLIT_SERVER_FILE_WATCHER_TYPE=none streamlit run streamlit_app.py
"""

import sqlite3
import time
from datetime import datetime
import os
import streamlit as st
from rag import answer_question

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "feedback.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            question TEXT,
            answer TEXT,
            feedback INTEGER,
            latency_seconds REAL,
            num_chunks INTEGER,
            top_source TEXT
        )
    """)
    conn.commit()
    conn.close()


def log_qa(question, answer, latency, num_chunks, top_source):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute(
        "INSERT INTO feedback (timestamp, question, answer, feedback, "
        "latency_seconds, num_chunks, top_source) VALUES (?, ?, ?, NULL, ?, ?, ?)",
        (datetime.now().isoformat(), question, answer, latency, num_chunks, top_source),
    )
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id


def update_feedback(row_id, value):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE feedback SET feedback = ? WHERE id = ?", (value, row_id))
    conn.commit()
    conn.close()


init_db()

st.set_page_config(page_title="Statistics Assistant", page_icon="📊")
st.title("📊 Engineering Statistics Assistant")
st.caption("Ask questions about process characterization, process modeling, and process monitoring. ")
st.caption("All answers are grounded in the [NIST/SEMATECH e-Handbook](https://www.itl.nist.gov/div898/handbook/toolaids/pff/index.htm).")
st.caption("Check out my [GitHub Repository](https://github.com/kang-mx/llm-zoomcamp/tree/main/capstone-project) for more!")
st.sidebar.markdown("[📈 View Monitoring Dashboard](https://llm-capstone-project-dashboard-kangmx.streamlit.app/)")

if "current_qa" not in st.session_state:
    st.session_state.current_qa = None
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = False

query = st.text_input("Your question", placeholder="e.g. What is a control chart used for?")
ask_clicked = st.button("Ask", type="primary")

if ask_clicked and query.strip():
    with st.spinner("Retrieving and generating answer..."):
        start = time.time()
        result = answer_question(query, search_type="hybrid", use_rewrite=False)
        latency = time.time() - start

        top_source = ""
        if result["retrieved_chunks"]:
            c = result["retrieved_chunks"][0]
            top_source = f"{c['source_doc']} p.{c['page']} [{c['section_title']}]"

        row_id = log_qa(query, result["answer"], latency, len(result["retrieved_chunks"]), top_source)

        st.session_state.current_qa = {
            "row_id": row_id,
            "question": query,
            "answer": result["answer"],
            "chunks": result["retrieved_chunks"],
            "latency": latency,
        }
        st.session_state.feedback_given = False

if st.session_state.current_qa:
    qa = st.session_state.current_qa
    st.markdown("### Answer")
    st.write(qa["answer"])
    st.caption(f"Answered in {qa['latency']:.2f}s using {len(qa['chunks'])} retrieved passages")

    with st.expander("View sources"):
        for c in qa["chunks"]:
            st.markdown(f"**{c['source_doc']} p.{c['page']} — {c['section_title']}** (RRF score: {c['score']:.3f})")
            st.text(c["text"][:300] + "...")
            st.divider()

    DOC_NAMES = {
        "ppc": "3. Production Process Characterization",
        "pmd": "4. Process Modeling",
        "pmc": "6. Process or Product Monitoring and Control",
    }
    st.info(
        "**Source key:**  \n" +
        "  \n".join(f"[`{code}`] {name}" for code, name in DOC_NAMES.items())
    )

    if not st.session_state.feedback_given:
        col1, col2, _ = st.columns([2, 2, 3])
        with col1:
            if st.button("👍 Helpful", use_container_width=True):
                update_feedback(qa["row_id"], 1)
                st.session_state.feedback_given = True
                st.rerun()
        with col2:
            if st.button("👎 Not helpful", use_container_width=True):
                update_feedback(qa["row_id"], -1)
                st.session_state.feedback_given = True
                st.rerun()
    else:
        st.success("Thanks for the feedback!")