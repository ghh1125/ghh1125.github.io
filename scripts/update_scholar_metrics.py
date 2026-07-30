import json
import re
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup


PROFILE_URLS = [
    "https://scholar.google.com/citations?user=S34GF9wAAAAJ&hl=en",
    "https://scholar.google.com/citations?user=S34GF9wAAAAJ&hl=zh-CN",
]
METRICS_PATH = Path("scholar-metrics.json")
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
    )
}


def parse_number(value):
    match = re.search(r"[0-9][0-9,]*", value or "")
    if not match:
        raise ValueError(f"Could not parse metric value: {value!r}")
    return int(match.group(0).replace(",", ""))


def fetch_metrics():
    last_error = None
    for url in PROFILE_URLS:
        try:
            response = requests.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.select_one("#gsc_rsb_st")
            if table is None:
                raise ValueError("Google Scholar metrics table was not found")

            values = {}
            for row in table.select("tr"):
                cells = row.select("td")
                if len(cells) < 2:
                    continue
                label = cells[0].get_text(" ", strip=True).lower()
                value = parse_number(cells[1].get_text(" ", strip=True))
                if "citation" in label or "引用" in label:
                    values["citations"] = value
                elif "h-index" in label or "h 指数" in label or "h指数" in label:
                    values["h_index"] = value
                elif "i10" in label:
                    values["i10_index"] = value

            required = {"citations", "h_index", "i10_index"}
            if required - values.keys():
                raise ValueError(f"Missing metrics: {sorted(required - values.keys())}")
            return values
        except (requests.RequestException, ValueError) as error:
            last_error = error

    raise RuntimeError(f"Unable to read Google Scholar profile: {last_error}")


def main():
    metrics = fetch_metrics()
    old = json.loads(METRICS_PATH.read_text()) if METRICS_PATH.exists() else {}
    if all(old.get(key) == value for key, value in metrics.items()):
        metrics["updated"] = old.get("updated", datetime.now(timezone.utc).date().isoformat())
    else:
        metrics["updated"] = datetime.now(timezone.utc).date().isoformat()
    METRICS_PATH.write_text(json.dumps(metrics, indent=2) + "\n")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
