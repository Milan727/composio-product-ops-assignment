import os
import re
import json
import time
import sys
import argparse
from pydantic import BaseModel
from typing import List
from google import genai
from google.genai import types

# Configurations
INPUT_FILE = "AI Product Ops Intern -The take-home assignment 054ba2edb94d83bb9e2f81974cac9c1c.md"
MODEL_NAME = "gemini-3.5-flash"

# Define Pydantic Schema for structured outputs
class AppDetails(BaseModel):
    one_line_description: str
    auth_methods: List[str]
    self_serve: str
    self_serve_details: str
    api_surface: str
    buildability_verdict: str
    buildability_blockers: str
    evidence_url: str
    mcp_exists: bool
    additional_notes: str

# Initialize Gemini Client
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY environment variable is not set.")
    sys.exit(1)

client = genai.Client(api_key=api_key)

def parse_assignment_apps():
    """Parses the markdown file to extract the list of 100 apps."""
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file {INPUT_FILE} not found.")
        sys.exit(1)
        
    with open(INPUT_FILE, "r") as f:
        content = f.read()
        
    # Split content by category sections
    categories = re.split(r'###\s+(\d+\.\s+[^|]+)', content)
    apps = []
    
    current_category = "Unknown"
    for part in categories:
        part = part.strip()
        if not part:
            continue
        
        # If it matches category header
        if re.match(r'^\d+\.\s+', part):
            current_category = re.sub(r'^\d+\.\s+', '', part).strip()
            continue
            
        # Parse table rows in this category part
        rows = re.findall(r'^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|', part, re.MULTILINE)
        for r in rows:
            app_id = int(r[0])
            app_name = r[1].strip()
            website_hint = r[2].strip()
            app_name_clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', app_name)
            
            apps.append({
                "id": app_id,
                "app_name": app_name_clean,
                "hint": website_hint,
                "category": current_category
            })
            
    return apps

def call_gemini_with_retry(model_client, prompt, max_retries=6, initial_backoff=6):
    backoff = initial_backoff
    for attempt in range(max_retries):
        try:
            response = model_client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=AppDetails,
                )
            )
            return json.loads(response.text.strip())
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "quota" in err_str.lower():
                print(f"Rate limit hit. Sleeping for {backoff} seconds before retry (Attempt {attempt+1}/{max_retries})...", flush=True)
                time.sleep(backoff)
                backoff *= 2  # Exponential backoff
            else:
                # Other exceptions (e.g. format issues), retry with same backoff or raise
                print(f"API Error: {e}. Retrying in {backoff} seconds...", flush=True)
                time.sleep(backoff)
                backoff *= 1.5
    raise Exception("Max retries exceeded for Gemini API call.")

def research_app(app, model_client):
    app_id = app["id"]
    app_name = app["app_name"]
    hint = app["hint"]
    category = app["category"]
    
    print(f"[{app_id}/100] Researching: {app_name} (Category: {category})", flush=True)
    
    prompt = f"""
You are an expert AI Product Operations Analyst.
Research the app "{app_name}" (Category: "{category}", Hint: "{hint}").
Provide details about its developer APIs, authentication, gating, and documentation based on your knowledge.

Instructions for fields:
1. "one_line_description": What this app does in one concise sentence.
2. "auth_methods": A list containing one or more of: "OAuth2", "API Key", "Basic", "Token", "Bearer Token", "HMAC", "Session", "None", or "Other".
3. "self_serve": Must be one of: "Self-serve" (free tier/trial or cheap plan developers can sign up for directly), "Gated" (requires partnership, sales contact, paid enterprise plan upfront, or admin approval), "Mixed" (some endpoints self-serve, some gated).
4. "self_serve_details": One-line explanation of the gating (e.g. "Free developer account with instant API key", "Requires contacting sales for enterprise access", "Free 14-day trial available").
5. "api_surface": Mention if it has REST, GraphQL, gRPC, or Webhooks, and scale (e.g. Broad REST API with hundreds of endpoints, Simple REST with 5 endpoints, GraphQL only).
6. "buildability_verdict": Must be one of: "Build-ready" (has public self-serve API, easily automated today), "Feasible with custom MCP" (needs custom setup, but technically possible without sales gates), "Blocked" (gated behind partnership, paid corporate plan, or no public API).
7. "buildability_blockers": Explain the main blockers (e.g. "None", "No public API", "Partner gated only", "Requires paid enterprise account to access API key").
8. "evidence_url": The exact official developer documentation URL or pricing link supporting these details. Make sure it is a valid HTTPS URL (e.g., https://developers.hubspot.com, etc.).
9. "mcp_exists": Boolean (true/false) indicating if there is an existing Model Context Protocol (MCP) server or Composio toolkit for this app.
10. "additional_notes": Any key developer insights.
"""

    try:
        result_json = call_gemini_with_retry(model_client, prompt)
        result_json["id"] = app_id
        result_json["app_name"] = app_name
        result_json["hint"] = hint
        result_json["category"] = category
        return result_json
        
    except Exception as e:
        print(f"Error calling Gemini for {app_name}: {e}", flush=True)
        # Return fallback values
        return {
            "id": app_id,
            "app_name": app_name,
            "hint": hint,
            "category": category,
            "one_line_description": "Failed to generate details",
            "auth_methods": ["Other"],
            "self_serve": "Gated",
            "self_serve_details": "Error during generation",
            "api_surface": "Unknown",
            "buildability_verdict": "Blocked",
            "buildability_blockers": "API Error during analysis",
            "evidence_url": hint,
            "mcp_exists": False,
            "additional_notes": f"Error: {e}"
        }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=100)
    parser.add_argument("--output", type=str, default="apps_research_v1.json")
    args = parser.parse_args()

    apps = parse_assignment_apps()
    apps = [a for a in apps if args.start <= a["id"] <= args.end]
    print(f"Running research for apps {args.start} to {args.end} ({len(apps)} apps)", flush=True)

    results = []
    if os.path.exists(args.output):
        try:
            with open(args.output, "r") as f:
                results = json.load(f)
            print(f"Loaded {len(results)} existing researched apps from {args.output}.", flush=True)
        except Exception as e:
            print(f"Failed to load existing output: {e}", flush=True)
            
    # Filter completed IDs to ignore fallback items
    completed_ids = set()
    filtered_results = []
    for r in results:
        is_fallback = (
            r.get("one_line_description") == "Failed to generate details" or
            "Error" in r.get("additional_notes", "") or
            "RESOURCE_EXHAUSTED" in r.get("additional_notes", "")
        )
        if not is_fallback and args.start <= r["id"] <= args.end:
            completed_ids.add(r["id"])
            filtered_results.append(r)
            
    print(f"Filtered out fallback/error entries. Clean completed count: {len(completed_ids)}/{len(apps)}")
    results = filtered_results
    
    for app in apps:
        if app["id"] in completed_ids:
            continue
            
        res = research_app(app, client)
        results.append(res)
        
        # Save results after each app to avoid losing progress
        try:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2)
        except Exception as e:
            print(f"Failed to write results: {e}", flush=True)
            
        # Cooling period to respect rate limits (longer sleep to be safe)
        time.sleep(1.5)
        
    # Sort results by ID before final save
    results.sort(key=lambda x: x["id"])
    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Completed slice {args.start}-{args.end}! Saved to {args.output}", flush=True)

if __name__ == "__main__":
    main()
