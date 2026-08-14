# PROJECT.md — Composio AI Product Ops Project Specification

## 1. Project Goal
Automate product ops research analyzing 100 enterprise SaaS apps for API accessibility, auth type, developer portal self-serve options, and tool buildability for AI agents and MCP (Model Context Protocol) toolkits.

## 2. Key Modules
- **Research Orchestrator (`research_agent.py`)**: Batches queries to Gemini 1.5 Pro API with strict Pydantic schemas and auto-resume.
- **Link & Logic Validator (`validator.py`)**: Asynchronously validates HTTP status codes for all developer documentation links.
- **Dataset (`apps_research_v2.json`)**: Final validated JSON dataset containing 100 SaaS applications.
- **Interactive UI (`index.html`)**: Interactive dark-mode dashboard displaying app search filters, buildability charts, and documentation links.

## 3. Environment Setup
```bash
export GEMINI_API_KEY="your-gemini-api-key"
```
