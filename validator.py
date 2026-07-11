import json
import os
import requests

INPUT_FILE = "apps_research_v2.json"
REPORT_FILE = "validation_report.md"

def load_data():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return []
    with open(INPUT_FILE, "r") as f:
        return json.load(f)

def check_url(url):
    if not url or not url.startswith("http"):
        return False, "Invalid URL format"
    try:
        # Use GET with stream=True or HEAD to be fast, but some servers block HEAD
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        res = requests.get(url, headers=headers, timeout=5, stream=True)
        if res.status_code >= 400:
            return False, f"HTTP Status {res.status_code}"
        return True, "OK"
    except Exception as e:
        return False, str(e)

def main():
    data = load_data()
    if not data:
        return

    print(f"Validating {len(data)} records...")
    issues = []
    
    for i, app in enumerate(data):
        app_id = app.get("id")
        name = app.get("app_name")
        verdict = app.get("buildability_verdict")
        blockers = app.get("buildability_blockers")
        self_serve = app.get("self_serve")
        evidence = app.get("evidence_url")
        auths = app.get("auth_methods", [])
        
        # Check 1: Missing critical fields
        missing = [k for k, v in app.items() if v is None or v == ""]
        if missing:
            issues.append({
                "id": app_id,
                "name": name,
                "type": "Missing Fields",
                "detail": f"Fields are empty: {missing}"
            })
            
        # Check 2: Verdict contradictions
        if verdict == "Build-ready" and self_serve == "Gated":
            issues.append({
                "id": app_id,
                "name": name,
                "type": "Contradiction",
                "detail": f"Verdict is 'Build-ready' but self_serve is 'Gated'."
            })
            
        if verdict == "Blocked" and (blockers == "None" or blockers == ""):
            issues.append({
                "id": app_id,
                "name": name,
                "type": "Contradiction",
                "detail": f"Verdict is 'Blocked' but blockers is '{blockers}'."
            })
            
        # Check 3: Empty auth methods
        if not auths or len(auths) == 0:
            issues.append({
                "id": app_id,
                "name": name,
                "type": "Contradiction",
                "detail": "Auth methods list is empty."
            })
            
        # Check 4: URL Check
        print(f"Checking URL for {name}...")
        ok, msg = check_url(evidence)
        if not ok:
            issues.append({
                "id": app_id,
                "name": name,
                "type": "Broken Link",
                "detail": f"Evidence URL failed: {evidence} ({msg})"
            })

    # Write report
    with open(REPORT_FILE, "w") as f:
        f.write("# Validation Report\n\n")
        f.write(f"Total apps checked: {len(data)}\n")
        f.write(f"Total issues found: {len(issues)}\n\n")
        
        if issues:
            f.write("| ID | App | Issue Type | Detail |\n")
            f.write("| --- | --- | --- | --- |\n")
            for iss in issues:
                f.write(f"| {iss['id']} | {iss['name']} | {iss['type']} | {iss['detail']} |\n")
        else:
            f.write("🎉 No logical issues or broken links found!\n")
            
    print(f"Validation complete! Report saved to {REPORT_FILE}")

if __name__ == "__main__":
    main()
