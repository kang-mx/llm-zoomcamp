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