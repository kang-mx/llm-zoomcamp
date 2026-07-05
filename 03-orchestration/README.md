# LLM Zoomcamp Module 3 Homework: AI Orchestration with Kestra

## Setup

1. **Docker check**
   ```bash
   docker --version && docker compose version
   ```

2. **Get the module files**
   This repo didn't originally include the course content, so the `03-orchestration` folder was pulled directly from the upstream course repo:
   ```bash
   cd /workspaces/llm-zoomcamp
   curl -L https://github.com/DataTalksClub/llm-zoomcamp/archive/refs/heads/main.tar.gz -o main.tar.gz
   tar -xzf main.tar.gz llm-zoomcamp-main/03-orchestration --strip-components=1
   rm main.tar.gz
   ```

3. **Get a Gemini API key**
   Visit https://aistudio.google.com/app/apikey, sign in, and create a key.

4. **Store the key in a `.env` file (not committed to git)**
   ```bash
   cd 03-orchestration
   echo -n "YOUR_REAL_GEMINI_KEY" | base64
   ```
   Create `.env` in `03-orchestration/`:
   ```
   GEMINI_API_KEY=YOUR_REAL_GEMINI_KEY
   SECRET_GEMINI_API_KEY=<base64 output from above>
   ```
   Added `.env` to `.gitignore` before any commit so the key is never pushed.

5. **Start Kestra**
   ```bash
   cd 03-orchestration
   docker compose up -d
   ```
   Kestra UI: http://localhost:8080

6. **Import the flows**
   ```bash
   curl -X POST -u 'admin@kestra.io:Admin1234!' http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/1_chat_without_rag.yaml
   curl -X POST -u 'admin@kestra.io:Admin1234!' http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/2_chat_with_rag.yaml
   curl -X POST -u 'admin@kestra.io:Admin1234!' http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/4_simple_agent.yaml
   ```

7. **Run flows in the Kestra UI**
   Namespace: `zoomcamp`. Executed `1_chat_without_rag`, `2_chat_with_rag`, and `4_simple_agent` (twice — once per `summary_length` setting, then a third time after modifying the flow for Q5).

## Answers

**Q1: Context Engineering** \
AI Copilot has access to current Kestra plugin documentation.

**Q2: RAG vs No RAG** \
Vague, generic, or fabricated — the model guesses from training data.
The non-RAG response listed plausible-sounding but incorrect Kestra 1.1 features (e.g. generic UI redesign, PDK enhancements, DuckDB plugin) that don't match the actual release. The RAG response correctly named real 1.1 features (No-Code Dashboard Editor, Multi-Agent AI Systems, Fix with AI, Human Task, improved air-gapped support).

**Q3: Token usage, short summary**

```
Multilingual Agent:
- Input tokens: 282
- Output tokens: 61
- Total tokens: 343

English Brevity Agent:
- Input tokens: 76
- Output tokens: 39
- Total tokens: 115
```
`multilingual_agent` output tokens: **61** → falls in the **60-100 tokens** range.

**Q4: Token usage, long summary**

```
Multilingual Agent:
- Input tokens: 282
- Output tokens: 187
- Total tokens: 469

English Brevity Agent:
- Input tokens: 202
- Output tokens: 50
- Total tokens: 252
```
`multilingual_agent` output tokens: **187** (vs. 61 for short).
Ratio around 3.07x which falls in the **2-5x more** range.

**Q5: Modifying a flow**

Changed `english_brevity` prompt from "exactly 1 sentence" to "exactly 3 sentences" (with `summary_length = long`).

```
Multilingual Agent:
- Input tokens: 282
- Output tokens: 198
- Total tokens: 480

English Brevity Agent:
- Input tokens: 213
- Output tokens: 95
- Total tokens: 308
```
- 1-sentence version: 50 output tokens
- 3-sentence version: 95 output tokens
- Ratio ≈ 1.9x → falls in the **2-4x more** range.

**Q6: Best Practices** \
Use traditional task-based workflows for predictability and auditability.
For regulated/compliance-heavy use cases (financial reporting, etc.), deterministic and auditable pipelines are preferable to agentic flexibility, which trades predictability for adaptability.

## Flow modification (Q5)

`english_brevity` task prompt changed from:
```yaml
prompt: |
  Generate exactly 1 sentence English summary of the following:
  "{{ outputs.multilingual_agent.textOutput }}"
```
to:
```yaml
prompt: |
  Generate exactly 3 sentences English summary of the following:
  "{{ outputs.multilingual_agent.textOutput }}"
```

Modified flow: `flows/4_simple_agent.yaml`