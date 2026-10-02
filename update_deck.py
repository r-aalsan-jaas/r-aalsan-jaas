import datetime
import urllib.request
import json
import re

username = "r-aalsan-jaas"

# 1. Fetch live public GitHub statistics
url = f"https://api.github.com/users/{username}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        public_repos = data.get("public_repos", 0)
        followers = data.get("followers", 0)
except Exception:
    public_repos = 2
    followers = 2

# 2. Get current UTC timestamp
now = datetime.datetime.now(datetime.timezone.utc)
time_str = now.strftime("%H:%M:%S UTC")

# 3. Read current bottom_deck.svg
with open("assets/bottom_deck.svg", "r", encoding="utf-8") as f:
    content = f.read()

# 4. Inject live values into the SVG text fields
# Replaces whatever is in the UPTIME and MEMORY text lines with live data
content = re.sub(
    r'(<text[^>]*>\s*UPTIME\s*</text>.*?<text[^>]*>)(.*?)(</text>)',
    rf'\g<1>{time_str}\g<3>',
    content,
    flags=re.DOTALL
)

content = re.sub(
    r'(<text[^>]*>\s*MEMORY\s*</text>.*?<text[^>]*>)(.*?)(</text>)',
    rf'\g<1>{public_repos} REPOS // {followers} FOLLOWERS\g<3>',
    content,
    flags=re.DOTALL
)

# 5. Save the updated SVG
with open("assets/bottom_deck.svg", "w", encoding="utf-8") as f:
    f.write(content)

print("Telemetry updated successfully.")
