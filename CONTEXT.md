# CONTEXT.md — Composio AI Product Ops Agent Context

## 1. System Overview
The **Composio Product Ops Agent** is an automated AI research pipeline and validation engine developed by **Milan Tiwari**. It queries the Google Gemini API with Pydantic structured schemas to research 100 enterprise SaaS applications for authentication mechanics, developer portal self-serve accessibility, and MCP (Model Context Protocol) tool buildability.

- **Repository**: [Milan727/composio-product-ops-assignment](https://github.com/Milan727/composio-product-ops-assignment)
- **Primary Stack**: Python 3.10+, `google-genai`, Pydantic v2, HTTPX / Requests, HTML5 / CSS3 / JavaScript (Data Dashboard).
- **Core Datasets**: `apps_research_v2.json` (Validated 100-app dataset), `validation_report.md`.

---

## 2. Developer Credentials
- **Author**: Milan Tiwari (Software & AI-Agentic Engineer)
- **GitHub**: [@Milan727](https://github.com/Milan727)

---

## 3. Directory & File Map
```
/
├── research_agent.py      # Main AI research agent (Gemini structured outputs & rate-limit retries)
├── validator.py           # Automated HTTP link checker & logic verification suite
├── fix_links.py           # Link cleaning script for automatic error correction
├── data_populator.py      # Populates research JSON outputs into formatted structures
├── apps_research_v2.json  # Final 100-app validated research dataset
├── index.html             # Interactive research matrix dashboard & analytics UI
├── validation_report.md   # Link check and validation error report
├── ARCHITECTURE.md        # Pipeline architecture, Pydantic schemas & state machine
└── PROJECT.md             # Project requirements & research metrics
```

---

## 4. AI Agent Guidelines & Rules
When extending or executing this research pipeline:

1. **Structured Output Enforcement**:
   - All Gemini responses MUST be strictly validated using Pydantic models in `research_agent.py`.
   - Never output un-typed JSON string blobs.

2. **Rate Limit Handling (`RESOURCE_EXHAUSTED` / 429)**:
   - Gemini API calls MUST implement exponential backoff retry loops (`time.sleep(2 ** attempt)`).

3. **Incremental State Saving**:
   - `research_agent.py` MUST save progress incrementally to avoid data loss on long batch runs.

4. **Environment Variables**:
   - Gemini API Key MUST be passed via `export GEMINI_API_KEY="..."` or `.env`.

---

## 5. Quick Development Commands
```bash
# Install dependencies
pip install google-genai pydantic requests

# Export API Key
export GEMINI_API_KEY="your-gemini-api-key"

# Run research on 100 apps
python3 research_agent.py

# Run verification & validation suite
python3 validator.py
```
