# LLM Zoomcamp

## Course Description
This is a practical course where I learn to build practical, production-ready LLM applications step by step. Over 10 weeks I'll learn Retrieval-Augmented Generation, vector search, embeddings, AI agents, function calling, evaluation, monitoring, hybrid search, reranking, and more.

Things I would learn:
- Module 1: Agentic RAG
    - Build a RAG pipeline with keyword search
    - Make it agentic with function calling
- Module 2: Vector Search
    - Semantic search with embeddings
    - minsearch, sqlitesearch, and PGVector
- Module 3: Orchestration
    - AI orchestration with Kestra
- Workshop: Data Ingestion
    - Pull traces from a monitoring service for analytics with dlt
- Module 4: Evaluation
    - Measure retrieval and answer quality
    - Offline and online evaluation
- Module 5: Monitoring
    - Monitor user feedback and system health
    - Live dashboards
- Module 6: Best Practices
    - LangChain
    - Hybrid search: combine vector and keyword search
    - Rerank results for higher precision
- Module 7: End-to-End Project
    - A complete project example: a fitness assistant built with LLMs

[2026 Cohort Homework](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026) \
[ML Zoomcamp Github](https://github.com/DataTalksClub/llm-zoomcamp) \
[My Github](https://github.com/kang-mx/llm-zoomcamp)


## Module 1: Introduction to Machine Learning

Learn the fundamentals: what what LLMs are and build a simple RAG pipeline using keyword search. Then make it agentic, so the LLM decides when and what to search instead of running a fixed pipeline.

Topics:
- What is RAG: Why LLMs need context, the RAG architecture
- Building a search engine with minsearch
- Building a prompt by combining search results
- RAG pipeline and RAG helper
- Data ingestion: persistent search with splitsearch
- Agents: Why a fixed RAG pipeline is not enough
- The Agentic Loop
- ToyAIKit: A teaching framework for the agent loop

Output:
- [Homework](https://github.com/kang-mx/llm-zoomcamp/tree/main/01-agentic-rag)
- [LinkedIn](https://www.linkedin.com/posts/kangmx_llmzoomcamp-aiengineering-rag-activity-7474826288713854976-f-hn)

References:
- [Stanford: Agents, Prompts & RAG](https://www.youtube.com/watch?v=k1njvbBmfsw)
- [LLM to Agent Skill (in Chinese)](https://www.youtube.com/watch?v=7qO8-kx3gW8&t=685s)
- [Databricks: What is RAG?](https://www.databricks.com/blog/what-is-retrieval-augmented-generation)
- [Gemini API quickstart](https://ai.google.dev/gemini-api/docs/quickstart)
- [Google LLMs](https://developers.google.com/machine-learning/crash-course/llm/transformers)
- [Attention is all you need](https://arxiv.org/pdf/1706.03762)


## Module 2: Vector Search

Vector search matches documents by semantic meaning instead of exact keyword overlap. We start from embeddings and end with persistent vector indexes (sqlitesearch, PGVector) and ONNX-based embedders for lightweight deployments.

Topics:
- Keyword search vs vector search, why it matters
- Embeddings: Turning text into vectors with sentence-transformers
- Vector search with numpy
- Vector Search with minsearch
- RAG with Vector Search
- Vector Search with sqlitesearch
- Vector Search with PGVector
- ONNX Embedder

Output:
- [Homework](https://github.com/kang-mx/llm-zoomcamp/tree/main/02-vector-search)

References:
- [Vector Search](https://www.ibm.com/think/topics/vector-search)
- [Embeddings (Google)](https://developers.google.com/machine-learning/crash-course/embeddings)
- [Embeddings (Open AI)](https://developers.openai.com/api/docs/guides/embeddings)
- [Embeddings: A Deep Dive from Basics to Advanced Concepts](https://medium.com/@sharanharsoor/embeddings-a-deep-dive-from-basics-to-advanced-concepts-f092765476fc)
- [Minsearch](https://pypi.org/project/minsearch/0.0.1/)
- [PGvector](https://www.databricks.com/blog/what-is-pgvector)
- [ONNX Embedding](https://github.com/chroma-core/onnx-embedding)


## Module 3: Orchestration

We learn how to orchestrate AI workflows using Kestra, an open-source orchestration platform. We start from the context problem that makes generic AI assistants unreliable, and end with autonomous multi-agent systems that can research, reason, and act without a fixed predetermined sequence of steps.

Topics:
- Using AI in workflows
- AI Copilot
- RAG Workflows
- Agentic Workflows

Output:
- [Homework](https://github.com/kang-mx/llm-zoomcamp/tree/main/03-orchestration)

References:
- [Meet Kestra in 65 seconds](https://www.youtube.com/watch?v=1DMXb98nTik)
- [Kestra Overview 2025](https://www.youtube.com/watch?v=xnGYiWFM2uk)
- [Kestra Beginner Tutorial](https://www.youtube.com/watch?v=bQNmXge5vSY)
- [Kestra Official Docs](https://kestra.io/docs)
- [Kestra Fundamentals](https://academy.kestra.io/kestra-fundamentals)
- [Kestra GitHub](https://github.com/kestra-io/kestra)
- [Introducing Kestra (from Medium)](https://medium.com/geekculture/introducing-kestra-finally-a-viable-airflow-alternative-fa664fdc7a0d)


## Module 4: Evaluation

This module covers systematic evaluation for search, RAG, and agent systems. We generate ground truth data with an LLM. Then we measure performance with Hit Rate, MRR, and LLM-as-a-judge.

Topics:
- Why evaluation matters, offline vs online
- Structured output for one document
- Batch generation, cost, and prepared data
- Search setup and relevance lists
- Hit Rate, MRR, the evaluate() function
- Using metrics to tune boost values
- RAG and Agent Evaluation
- Using an LLM to evaluate answer quality
- Agent Evaluation

Output:
- [Homework](https://github.com/kang-mx/llm-zoomcamp/tree/main/04-evaluation)

References:
- [LLM Evaluation: A beginner's guide](https://www.evidentlyai.com/llm-guide/llm-evaluation)
- [LLM as a judge](https://opensearch.org/blog/introducing-llm-as-a-judge-scaling-search-relevance-evaluation-with-ai/)
- [LLM Evaluation Framework: Trajectories vs Outputs](https://www.langchain.com/resources/llm-evaluation-framework)
- [RAG & LLM Evaluation Tools](https://medium.com/@zilliz_learn/top-10-rag-llm-evaluation-tools-you-dont-want-to-miss-a0bfabe9ae19)
- [LLM Evaluation & Agent Evaluation](https://mlflow.org/llm-evaluation)
- [How Hit Rate & MRR Measure LLM Retrievers](https://tamilselvan-subramanian.medium.com/how-hit-rate-and-mrr-measure-llm-retrievers-ai-simplified-series-7203ba2d4032)
- [Ground Truth Generation for LLMs](https://medium.com/@adarsh_sh/simplifying-ground-truth-generation-for-llms-f04e8257c4ec)


## Module 5: Monitoring

Offline evaluation can't tell you how your RAG system performs once real people use it. This module covers online monitoring: collecting metrics from real traffic and visualizing them on a dashboard. 

We build a Streamlit chat app, capture metrics, store conversations in PostgreSQL, and create Grafana dashboards for real-time monitoring.

Topics:
- Setting up the RAG assistant
- Basic Streamlit app with RAG
- LLMCallRecord, cost tracking
- PostgreSQL with Docker, saving conversations
- Querying Data
- Streamlit Dashboard
- User Feedback
- LLM-as-a-judge for automatic relevance evaluation
- Feedback Dashboard
- Grafana Dashboards
- Docker Compose

Output:
- [Homework](https://github.com/kang-mx/llm-zoomcamp/tree/main/05-monitoring)

References:
- [Connect Streamlit to PostgreSQL](https://docs.streamlit.io/develop/tutorials/databases/postgresql)
- [LLM Observability](https://medium.com/@vasanthancomrads/opentelemetry-for-llm-observability-foundations-architecture-and-your-first-instrumented-llm-6bb1d3dc3cc6)
- [PostgreSQL in Docker](https://www.datacamp.com/tutorial/postgresql-docker)
- [Dashboard in Python using Streamlit](https://discuss.streamlit.io/t/building-a-dashboard-in-python-using-streamlit/60621)
- [LLM as a Judge RAG](https://www.datacamp.com/tutorial/llm-as-a-judge-rag)
- [LLM Synthetic Data](https://www.evidentlyai.com/llm-guide/llm-test-dataset-synthetic-data)
- [Grafana SQL Data Source](https://grafana.com/docs/grafana/latest/datasources/postgres/)