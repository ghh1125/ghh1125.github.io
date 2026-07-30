# Hanghui Guo's Homepage

This repository contains the static academic homepage of Hanghui Guo, built from the [IsakZhang/isakzhang.github.io](https://github.com/IsakZhang/isakzhang.github.io) layout.

The site is published through GitHub Pages. Update the HTML pages and `site.js`, then push to the `master` branch to publish changes.

## Automatic Google Scholar metrics

The `google-scholar-crawler` workflow runs after a Pages build and every day at
08:00 UTC (16:00 Beijing time). It publishes `gs_data.json` and a Shields.io
badge payload to the `google-scholar-stats` branch. The homepage reads that
branch first and falls back to `scholar-metrics.json` if the branch is not
available yet.

Before enabling the workflow, add this repository Actions secret:

- Name: `GOOGLE_SCHOLAR_ID`
- Value: `S34GF9wAAAAJ`

Because GitHub-hosted runner IPs can receive a 403 from Google Scholar, add a
second secret for the proxy-backed crawl:

- Name: `SCRAPERAPI_KEY`
- Value: your ScraperAPI key

The workflow uses ScraperAPI when this secret is present and otherwise tries
the public Scholar domains directly.

The workflow also has this public ID as a fallback, so a temporary secret
configuration problem will not stop the crawler.

You can also run the workflow manually from **Actions → Update Google Scholar
citation data → Run workflow**. The crawler updates once per run; Google
Scholar itself does not provide a second-by-second live feed.

## Pages

- `index.html` — About and research interests
- `research.html` — Publications
- `group.html` — Honors and academic service
- `getinvolved.html` — Teaching, internship, and contact
