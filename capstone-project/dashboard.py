"""
Monitoring dashboard for the handbook RAG assistant.
Reads from feedback.db (populated by streamlit_app.py) and shows usage,
quality, and performance metrics.

Usage:
    streamlit run dashboard.py
"""

import sqlite3
import pandas as pd
import streamlit as st
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "feedback.db")

st.set_page_config(page_title="Monitoring Dashboard", page_icon="📈", layout="wide")
st.title("📈 RAG Assistant: Monitoring Dashboard")

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM feedback", conn)
conn.close()

if df.empty:
    st.warning("No data yet. Ask a few questions in the main app first.")
    st.stop()

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["source_doc"] = df["top_source"].str.split(" p\\.").str[0]

# --- Summary metrics ---
total_q = len(df)
feedback_given = df["feedback"].notna().sum()
positive = (df["feedback"] == 1).sum()
negative = (df["feedback"] == -1).sum()
satisfaction = positive / feedback_given if feedback_given else 0
avg_latency = df["latency_seconds"].mean()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total questions", total_q)
c2.metric("Feedback given", f"{feedback_given} ({feedback_given/total_q:.0%})")
c3.metric("Satisfaction rate", f"{satisfaction:.0%}")
c4.metric("Avg. latency", f"{avg_latency:.2f}s")

st.divider()

col_a, col_b = st.columns(2)

# Chart 1: feedback breakdown
with col_a:
    st.subheader("Feedback breakdown")
    feedback_counts = pd.Series({
        "Helpful": positive,
        "Not helpful": negative,
        "No feedback": total_q - feedback_given,
    })
    st.bar_chart(feedback_counts)

# Chart 2: latency distribution
with col_b:
    st.subheader("Response latency distribution")
    st.bar_chart(df["latency_seconds"].round(1).value_counts().sort_index())

col_c, col_d = st.columns(2)

# Chart 3: questions over time
with col_c:
    st.subheader("Questions over time")
    by_time = df.set_index("timestamp").resample("h").size()
    st.line_chart(by_time)

# Chart 4: most-referenced source documents
with col_d:
    st.subheader("Most-referenced documents")
    st.bar_chart(df["source_doc"].value_counts())

# Chart 5: rolling satisfaction rate over question sequence
st.subheader("Satisfaction rate over time (rolling avg, last 10 rated questions)")
rated = df[df["feedback"].notna()].sort_values("timestamp").copy()
if len(rated) >= 2:
    rated["feedback_pct"] = (rated["feedback"] == 1).astype(int)
    rated["rolling_satisfaction"] = rated["feedback_pct"].rolling(10, min_periods=1).mean()
    st.line_chart(rated.set_index("timestamp")["rolling_satisfaction"])
else:
    st.info("Not enough rated questions yet to show a trend.")

st.divider()
st.subheader("Recent questions")
st.dataframe(
    df.sort_values("timestamp", ascending=False)
      [["timestamp", "question", "feedback", "latency_seconds", "source_doc"]]
      .head(20),
    use_container_width=True,
)