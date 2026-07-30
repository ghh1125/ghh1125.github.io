import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import requests


scholar_id = os.environ.get("GOOGLE_SCHOLAR_ID") or "S34GF9wAAAAJ"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "Chrome/126.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}
response = None
profile_url = None
errors = []
for host in (
    "scholar.google.com",
    "scholar.google.co.uk",
    "scholar.google.ca",
    "scholar.google.com.au",
):
    candidate_url = f"https://{host}/citations?user={scholar_id}&hl=en"
    try:
        candidate = requests.get(candidate_url, headers=headers, timeout=30)
        candidate.raise_for_status()
        response = candidate
        profile_url = candidate_url
        break
    except requests.RequestException as error:
        errors.append(f"{host}: {error}")

if response is None:
    raise RuntimeError("All Google Scholar endpoints failed: " + " | ".join(errors))

table_match = re.search(
    r'<table id="gsc_rsb_st".*?</table>', response.text, flags=re.DOTALL
)
if not table_match:
    raise RuntimeError("Google Scholar metrics table was not found")

values = [
    int(value.replace(",", ""))
    for value in re.findall(
        r'class="gsc_rsb_std">([0-9][0-9,]*)</td>', table_match.group(0)
    )
]
if len(values) < 5:
    raise RuntimeError(f"Expected Scholar metrics, found: {values}")

author = {
    "scholar_id": scholar_id,
    "name": "Hanghui Guo",
    "citedby": values[0],
    "hindex": values[2],
    "i10index": values[4],
    "updated": datetime.now(timezone.utc).isoformat(),
    "profile_url": profile_url,
    "publications": {},
}

results = Path("results")
results.mkdir(exist_ok=True)
(results / "gs_data.json").write_text(
    json.dumps(author, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
(results / "gs_data_shieldsio.json").write_text(
    json.dumps(
        {
            "schemaVersion": 1,
            "label": "citations",
            "message": str(author["citedby"]),
        },
        ensure_ascii=False,
    )
    + "\n",
    encoding="utf-8",
)

print(json.dumps(author, ensure_ascii=False, indent=2))
