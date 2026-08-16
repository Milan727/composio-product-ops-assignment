# AI Agent Toolkit & API Gating Intelligence Platform

> **Author**: Milan Tiwari | **Domain**: [milantiwari.in](https://milantiwari.in) | **Live Platform**: [milantiwari.in/projects](https://milantiwari.in/projects)

An automated research engine, dataset, and interactive intelligence platform designed to analyze 100 enterprise SaaS applications for auth mechanics, self-serve developer credential access, API surface scope, and buildability metrics for AI agent toolkits (Model Context Protocol / Composio).

---

## 🌐 Live Platform & Interactive Matrix
Explore the live interactive dashboard, category filters, and detailed developer notes:
* ⚡ **Live Web Platform**: [milantiwari.in/projects](https://milantiwari.in/projects)

---

## 🛠️ Repository Architecture
* `index.html`: Sleek, responsive dark-mode dashboard with Client-Side Search, Category Filtering, Chart.js Visualizations, and Modal Deep-Dives.
* `apps_research_v2.json`: Final validated dataset covering 100 enterprise apps across 10 verticals.
* `research_agent.py`: Python research agent executing structured Pydantic model outputs via the Gemini API with exponential backoff retries.
* `validator.py`: Automated validation suite performing HTTP HEAD/GET status code checks (200 OK) and logical consistency assertions.
* `fix_links.py`: Data cleaning pipeline resolving broken/outdated documentation paths.

---

## ⚙️ How to Run the Research Agent

### 1. Install Dependencies
```bash
pip3 install google-genai pydantic requests
```

### 2. Set Up Gemini API Key
```bash
export GEMINI_API_KEY="your-gemini-api-key"
```

### 3. Run the Research Agent
```bash
# Process all 100 apps with automatic resume & rate-limit backoff
python3 research_agent.py

# Process specific sub-ranges
python3 research_agent.py --start 1 --end 25 --output apps_part1.json
```

### 4. Execute the Validation Suite
```bash
python3 validator.py
```

---

## 📊 Summary Metrics

* **Apps Analyzed**: 100 enterprise SaaS platforms across 10 industry categories
* **Build-Ready (Instant Self-Serve Credentials)**: 82%
* **Blocked (Enterprise Gating / Partner Program required)**: 16%
* **Feasible (Manual Setup / Custom Tokens)**: 2%
* **Dominant Auth Standards**: Bearer Tokens (67%), OAuth 2.0 (56%), API Keys (47%)
* **MCP / Agent Toolkit Compatibility**: 80%
