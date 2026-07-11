# AI Product Ops Research Agent & Case Study

This repository contains the automated research pipeline, dataset, and interactive case study dashboard designed to analyze 100 enterprise apps for auth mechanics, self-serve credentials access, and buildability metrics for AI agent toolkits (MCP servers/Composio).

## 🚀 Deployed Case Study Dashboard
The final research results are built into a premium, responsive web app:
* **Interactive Matrix**: [index.html](index.html) (Search, filter, and view detailed developer notes for all 100 apps).

---

## 🛠️ Project Structure
* `research_agent.py`: The Python research agent that reads apps from the assignment sheet and queries the Gemini API with structured outputs and exponential retry logic.
* `validator.py`: Automated validation script checking link status codes and logical contradictions.
* `fix_links.py`: Data cleaning script executing verification corrections based on validation reports.
* `apps_research_v2.json`: The final, validated 100-app dataset.
* `index.html`: Sleek dark-mode web dashboard visualizing patterns, metrics, process charts, and the interactive dataset.

---

## ⚙️ How to Run the Research Agent

### 1. Install Dependencies
Make sure you have Python 3.10+ installed. Install the required libraries using pip:
```bash
pip3 install google-genai pydantic requests
```

### 2. Configure the Gemini API Key
Obtain an API key from [Google AI Studio](https://aistudio.google.com/) and export it to your environment variables:
```bash
export GEMINI_API_KEY="your-gemini-api-key"
```

### 3. Run the Research Agent
Run the main script. You can run it on the whole set of 100 apps, or process specific ranges using slices:
```bash
# Run on all 100 apps (default)
python3 research_agent.py

# Run a specific range (e.g., apps 1 to 25) saving to a custom part file
python3 research_agent.py --start 1 --end 25 --output apps_part1.json
```
The script features **automatic resuming** and skips any already parsed items. It also handles API rate limits (`429 RESOURCE_EXHAUSTED`) using exponential backoff retries.

### 4. Run the Data Validation Suite
Verify data integrity, check for logical conflicts, and test all documentation links for live status codes (200 OK):
```bash
python3 validator.py
```
This writes a summary of flagged items (e.g., broken URLs) to `validation_report.md`.

---

## 📊 Summary of Findings

* **Total Apps Analysed**: 100
* **Build-Ready (Instant API Access)**: 82%
* **Blocked (Gated/Paid Account required)**: 16%
* **Feasible (Manual approval/Setup required)**: 2%
* **Dominant Auth Types**: Bearer Token (67%), OAuth2 (56%), API Key (47%)
* **MCP Integration Exists**: 80% (80 apps have active Composio tools or community MCP configurations)
