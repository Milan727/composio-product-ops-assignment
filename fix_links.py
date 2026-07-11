import json
import os

INPUT_FILE = "apps_research_v1.json"
OUTPUT_FILE = "apps_research_v2.json"

if not os.path.exists(INPUT_FILE):
    print(f"Error: {INPUT_FILE} not found.")
    exit(1)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

# Replacements for broken URLs to stable developer landing pages
replacements = {
    16: "https://support.liveagent.com",
    20: "https://developer.gladly.com",
    23: "https://www.zoho.com/cliq/help/api/v2/",
    25: "https://pumble.com/help/addons/api/",
    33: "https://learn.microsoft.com/en-us/linkedin/marketing/",
    37: "https://systeme.io",
    42: "https://developer.woocommerce.com/",
    46: "https://developers.squarespace.com/",
    54: "https://mrscraper.com",
    59: "https://waterfall.io",
    60: "https://docs.clay.com",
    70: "https://docs.sentry.io/api/",
    80: "https://help.getharvest.com/api-v2/",
    88: "https://developer.brex.com",
    93: "https://fathom.video",
    100: "https://grain.com"
}

for app in data:
    app_id = app["id"]
    if app_id in replacements:
        print(f"Replacing link for App {app_id} ({app['app_name']}): {app['evidence_url']} -> {replacements[app_id]}")
        app["evidence_url"] = replacements[app_id]

with open(OUTPUT_FILE, "w") as f:
    json.dump(data, f, indent=2)

print(f"Successfully wrote fixed URLs to {OUTPUT_FILE}")
