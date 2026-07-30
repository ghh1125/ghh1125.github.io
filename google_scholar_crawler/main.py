import json
import os
from datetime import datetime, timezone
from pathlib import Path

from scholarly import scholarly


scholar_id = os.environ.get("GOOGLE_SCHOLAR_ID")
if not scholar_id:
    raise RuntimeError(
        "GOOGLE_SCHOLAR_ID is missing. Add it as a repository Actions secret."
    )

author = scholarly.search_author_id(scholar_id)
scholarly.fill(author, sections=["basics", "indices", "counts", "publications"])
author["updated"] = datetime.now(timezone.utc).isoformat()
author["publications"] = {
    publication["author_pub_id"]: publication
    for publication in author.get("publications", [])
    if publication.get("author_pub_id")
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
            "message": str(author.get("citedby", 0)),
        },
        ensure_ascii=False,
    )
    + "\n",
    encoding="utf-8",
)

print(json.dumps(author, ensure_ascii=False, indent=2))
