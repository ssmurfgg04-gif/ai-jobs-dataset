# AI/ML Remote Jobs Dataset

**Weekly-refreshed dataset of 500+ active remote AI/ML jobs with salary data, tech stack, and direct application links.**

[Buy on Gumroad](https://smurfglow.gumroad.com/l/kqtaiu)

## Dataset Contents

Each weekly update (~500+ jobs) includes:

| Field | Description |
|-------|-------------|
| Company Name | Hiring organization |
| Job Title | Role title |
| Location | Remote policy + geographic restrictions |
| Salary Min | Minimum salary (when listed) |
| Salary Max | Maximum salary (when listed) |
| Tech Stack | Required skills & technologies |
| Job URL | Direct application link |
| Date Posted | When the role was listed |
| Source | Platform where it was found |
| Company Industry | Sector |
| Company Employee Count | Organization size |

## Sources

| Source | Type | Coverage |
|--------|------|----------|
| LinkedIn | Board | Global |
| Indeed | Board | Global |
| Glassdoor | Board | Global |
| RemoteOK | Remote board | Worldwide |
| Remotive | Remote board | Worldwide |
| WeWorkRemotely | Remote board | Worldwide |
| HackerNews | Community | Global |
| X/Twitter | Community | Global |
| Greenhouse | ATS | Tech companies |
| Lever | ATS | Tech companies |
| Workable | ATS | Tech companies |
| Ashby | ATS | Tech companies |

## Data Formats

- **CSV** — Open in any spreadsheet or data tool
- **JSON** — For programmatic use
- **Excel (.xlsx)** — Formatted with filters + styling

## Pricing

| Tier | Price | What You Get |
|------|-------|-------------|
| Single Snapshot | $19 | One week of data |
| Annual Subscription | $49 | 52 weekly updates |

## Updates

New data every Monday by 9 AM UTC.

## Pipeline

The scraper runs automatically via GitHub Actions. It:
1. Scrapes all 12+ sources
2. Filters for AI/ML relevance
3. Deduplicates and cleans
4. Removes non-remote roles
5. Outputs CSV + JSON + Excel

[View pipeline](.github/workflows/scrape.yml)

## Tech Stack

Built with Python, pandas, GitHub Actions. Forked from [Harsh-C7/JobScraper](https://github.com/Harsh-C7/JobScraper).

## License

Dataset: Commercial use allowed for purchasers.
Code: MIT
