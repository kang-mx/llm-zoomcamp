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
- [LinkedIn]()

References:
- [Find median](https://stackoverflow.com/questions/24101524/finding-median-of-list-in-python)
- [Fill in blank rows](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html)
- [Get first N](https://www.geeksforgeeks.org/pandas/get-first-n-records-of-a-pandas-dataframe/)
- [Sum of array](https://www.geeksforgeeks.org/dsa/program-find-sum-elements-given-array/)