# 🌍 JobScraper — Find Your Ideal Remote Job, Automatically

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Output-Excel%20(.xlsx)-brightgreen?style=for-the-badge&logo=microsoft-excel" />
  <img src="https://img.shields.io/badge/Remote%20Jobs-Only-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Contributions-Welcome-blueviolet?style=for-the-badge" />
</p>

> **A fully automated, multi-source job scraping engine** that aggregates remote job listings from LinkedIn, Indeed, Glassdoor, HackerNews, X (Twitter), Remotive, RemoteOK, WeWorkRemotely, Greenhouse, Lever, Workable, and Ashby — filters out fake remote jobs — and delivers a clean, deduplicated, formatted Excel spreadsheet of **only the companies that are truly open to hiring you worldwide.**

---

## 📖 Table of Contents

- [Why JobScraper?](#-why-jobscraper)
- [How It Works](#-how-it-works)
- [Sources Scraped](#-sources-scraped)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration — Customize For Your Job Search](#️-configuration--customize-for-your-job-search)
- [Running the Scraper](#-running-the-scraper)
- [Understanding the Output](#-understanding-the-output)
- [How to Adapt This for Your Own Needs](#-how-to-adapt-this-for-your-own-needs)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🤔 Why JobScraper?

Finding a **genuinely remote, worldwide-open** tech job is hard. Most job boards are flooded with:
- "Remote" jobs that are actually US-only or EU-only
- Listings you've already seen and applied to
- Roles that don't match your tech stack

**JobScraper solves all three problems:**

1. **Aggregates** job listings from **10+ sources** in one run
2. **Filters** out fake-remote / geo-restricted roles using a scoring engine
3. **Deduplicates** so you only see fresh, unique companies — every run
4. **Remembers** previously seen jobs (via a local SQLite database) so you never see the same listing twice across multiple runs
5. **Exports** a clean, formatted Excel file ready to review and act on

---

## ⚙️ How It Works

The scraper runs in **4 sequential phases**, each targeting a different category of job source:

```
┌─────────────────────────────────────────────────────────────────┐
│                        PHASE 1: Community Sources                │
│   HackerNews "Who is Hiring?" thread  +  X/Twitter (via DDG)    │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                  PHASE 2: Remote Niche Job Boards                │
│         Remotive API  +  RemoteOK API  +  WeWorkRemotely RSS     │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│              PHASE 3: True Remote Filtering Engine               │
│   Scores every job description using RED FLAGS / GREEN FLAGS     │
│   Removes "Fake Remote" (US-only, clearance required, etc.)      │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│             PHASE 4: ATS Direct Platforms (Google Dorking)       │
│    Greenhouse  +  Lever  +  Workable  +  Ashby (via DuckDuckGo)  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│              MAINSTREAM BOARDS (LinkedIn / Indeed / Glassdoor)   │
│     Uses python-jobspy to scrape across locations & roles        │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                    STATE MANAGER (SQLite)                        │
│   Hashes each job (URL or Company+Title) and removes any job     │
│   you've already seen in a previous run                          │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                  OUTPUT: Formatted Excel (.xlsx)                 │
│   remote_companies_hiring_YYYY-MM-DD_HHMM.xlsx                  │
│   Includes: Company, Role, Location, Salary, URL, Remote Status  │
└─────────────────────────────────────────────────────────────────┘
```

### 🔴 Red Flags (Jobs that get filtered OUT)
The `true_remote_filter.py` engine removes listings that contain phrases like:
- `"US only"`, `"United States only"`, `"must reside in the US"`
- `"UK only"`, `"Europe only"`
- `"No visa sponsorship"`, `"US citizen"`, `"W2 only"`
- `"Security clearance"`, `"Cleared candidates"`

### 🟢 Green Flags (Jobs that get BOOSTED in ranking)
- `"Work from anywhere"`, `"Anywhere in the world"`, `"Global team"`
- `"Worldwide"`, `"Remote India"`, `"Distributed team"`, `"Digital nomad"`

Each job gets a **Remote Score**. Jobs with a score below `-5` are dropped. Verified worldwide jobs appear at the top of the output.

---

## 🌐 Sources Scraped

| Source | Type | Method |
|---|---|---|
| **LinkedIn** | Mainstream board | `python-jobspy` |
| **Indeed** | Mainstream board | `python-jobspy` |
| **Glassdoor** | Mainstream board | `python-jobspy` |
| **HackerNews** (Who is Hiring?) | Community | HN Firebase API |
| **X / Twitter** | Community | DuckDuckGo search dorking |
| **Remotive** | Remote niche board | Official REST API |
| **RemoteOK** | Remote niche board | Official REST API |
| **WeWorkRemotely** | Remote niche board | RSS Feed |
| **Greenhouse** | ATS direct | DuckDuckGo search dorking |
| **Lever** | ATS direct | DuckDuckGo search dorking |
| **Workable** | ATS direct | DuckDuckGo search dorking |
| **Ashby** | ATS direct | DuckDuckGo search dorking |

---

## 📁 Project Structure

```
JobScraper/
│
├── scraper.py                  # 🚀 Main entry point — orchestrates all phases
├── config.json                 # ⚙️  YOUR configuration file (edit this!)
│
├── hn_scraper.py               # HackerNews "Who is Hiring?" scraper
├── twitter_scraper.py          # X/Twitter job scraper via DuckDuckGo
├── remote_boards_scraper.py    # Remotive + RemoteOK + WeWorkRemotely
├── ats_scraper.py              # Greenhouse / Lever / Workable / Ashby via DDG
│
├── true_remote_filter.py       # 🔍 Red/Green flag scoring engine
├── state_manager.py            # 💾 SQLite-based "seen jobs" deduplication
│
├── jobs_state.db               # Auto-generated SQLite DB (gitignored)
└── remote_companies_hiring_*.xlsx  # Auto-generated output (gitignored)
```

---

## 📋 Prerequisites

- **Python 3.9 or higher**
- **pip** (comes with Python)
- A working internet connection

No API keys required. All sources are scraped using public APIs, RSS feeds, or search dorking.

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Harsh-C7/JobScraper.git
cd JobScraper
```

### 2. (Recommended) Create a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

The scraper will **auto-install** missing Python packages on first run. But if you prefer to install manually:

```bash
pip install pandas python-jobspy openpyxl beautifulsoup4 duckduckgo-search tqdm requests
```

---

## ⚙️ Configuration — Customize For Your Job Search

All customization happens in a single file: **`config.json`**

```json
{
  "search_terms": [
    "software engineer remote",
    "full stack developer remote",
    "backend developer remote",
    "python developer remote",
    "react developer remote",
    "node.js remote"
  ],
  "tech_skills": [
    "react",
    "next.js",
    "nextjs",
    "python",
    "node.js",
    "nodejs",
    "full stack"
  ],
  "jobspy_platforms": ["linkedin", "indeed", "glassdoor"],
  "jobspy_target_locations": ["USA", "Europe", "UK"],
  "jobspy_results_wanted": 1000,
  "jobspy_hours_old": 72
}
```

### Configuration Reference

| Field | Description | Example |
|---|---|---|
| `search_terms` | Job titles / roles to search for on mainstream boards (LinkedIn, Indeed, Glassdoor) | `"python developer remote"` |
| `tech_skills` | Keywords to match against job descriptions and community sources | `"react"`, `"django"`, `"rust"` |
| `jobspy_platforms` | Which mainstream platforms to scrape | `"linkedin"`, `"indeed"`, `"glassdoor"` |
| `jobspy_target_locations` | Geo-targets for mainstream board searches | `"USA"`, `"Europe"`, `"UK"`, `"Canada"` |
| `jobspy_results_wanted` | Max results to fetch per search term per platform | `500` |
| `jobspy_hours_old` | Only fetch jobs posted within this many hours | `72` (= last 3 days) |

---

## 🎯 How to Adapt This for Your Own Needs

### 🔧 Change Your Tech Stack

Edit `tech_skills` in `config.json` to match your skillset:

```json
"tech_skills": ["golang", "rust", "kubernetes", "devops", "terraform"]
```

These keywords are matched against job descriptions across **all scraped sources** — HackerNews comments, ATS listings, Remotive, RemoteOK, and more.

### 🔍 Change the Roles You're Looking For

Edit `search_terms` for the mainstream job boards:

```json
"search_terms": [
  "devops engineer remote",
  "site reliability engineer remote",
  "platform engineer remote"
]
```

### 🌍 Change the Target Regions

Edit `jobspy_target_locations` to focus on specific geographies when searching LinkedIn/Indeed:

```json
"jobspy_target_locations": ["USA", "Canada", "Australia"]
```

> **Note:** This doesn't restrict which jobs you'll be _eligible_ for — that's handled by the True Remote Filter. This controls the geographic context used when querying mainstream job boards.

### 🕐 Control How Fresh the Jobs Are

Adjust `jobspy_hours_old` to widen or narrow the time window:

```json
"jobspy_hours_old": 24    // Only jobs from the last 24 hours
"jobspy_hours_old": 168   // Jobs from the last 7 days
```

### 🚩 Add or Remove Remote Restriction Keywords

Edit the `RED_FLAGS` and `GREEN_FLAGS` lists in [`true_remote_filter.py`](true_remote_filter.py):

```python
# Add a new red flag to filter out jobs that require EU tax residency
RED_FLAGS = [
    ...
    r'eu tax residency required',
]

# Add a new green flag to boost jobs that mention your country
GREEN_FLAGS = [
    ...
    r'remote pakistan',
    r'remote brazil',
]
```

### 🏢 Add New ATS Platforms

In [`ats_scraper.py`](ats_scraper.py), add new ATS domains to the `platforms` list:

```python
platforms = [
    "boards.greenhouse.io",
    "jobs.lever.co",
    "apply.workable.com",
    "jobs.ashbyhq.com",
    "jobs.rippling.com",   # ← add new ATS platforms here
]
```

### 📋 Add New Remote Job Boards

In [`remote_boards_scraper.py`](remote_boards_scraper.py), add a new function following the existing pattern and call it inside `fetch_remote_boards()`:

```python
def fetch_mynewboard_jobs(tech_skills):
    # Fetch from your new board's API or RSS
    ...
    return jobs  # list of dicts with standard keys

def fetch_remote_boards(search_terms):
    ...
    # Add your new source here:
    new_jobs = fetch_mynewboard_jobs(tech_skills)
    if new_jobs: all_jobs.extend(new_jobs)
```

The expected keys for each job dict are:
```python
{
    'company': str,
    'title': str,
    'location': str,
    'job_url': str,
    'date_posted': str or datetime,
    'site': str,
    'company_industry': str,
    'company_num_employees': int or None,
    'min_amount': float or None,
    'max_amount': float or None,
    'description': str
}
```

### 🧹 Reset Your "Seen Jobs" History

The state manager (`jobs_state.db`) remembers every job it has ever shown you so duplicates don't appear in future runs. To reset this memory (e.g., to do a fresh search):

```bash
# Simply delete the database file
del jobs_state.db         # Windows
rm jobs_state.db          # macOS / Linux
```

---

## ▶️ Running the Scraper

```bash
python scraper.py
```

The scraper will print live progress to your terminal and may take **5–20 minutes** depending on your internet speed and the number of sources being scraped.

**Sample output:**

```
--- Starting job scraping process ---
Scraping HackerNews: Who is Hiring...
Found 'Who is Hiring' post ID 43123456. Fetching comments...
Processing comments...
Parsing HackerNews: 100%|████████████████| 623/623 [02:14<00:00]
Scraped 47 matching HackerNews jobs.

Scraping X/Twitter via DuckDuckGo Search (Dorking)...
Querying Twitter/X: 100%|███████████████| 12/12 [00:23<00:00]
Scraped 18 matching X/Twitter jobs.

--- Starting Phase 2: Remote Niche Job Boards ---
Scraping Remotive API...
Scraping RemoteOK API...
Scraping WeWorkRemotely RSS feed...
Phase 2 Complete: Scraped 63 matching jobs from Remote Boards.

Scraping top-tier ATS platforms (Greenhouse, Lever, Workable, Ashby)...
Searching ATS Platforms: 100%|██████████| 24/24 [00:38<00:00]
Phase 4 Complete: Scraped 92 global roles directly from ATS platforms.

Scraping linkedin for 'software engineer remote' in 'USA'...
Scraped 150 results from linkedin
...

Total raw results collected: 1284
After deduplication: 743 unique companies

--- Starting Phase 3: True Remote Filtering Engine ---
Fetching deeper job descriptions for 128 raw links...
Downloading Missing JDs: 100%|██████████| 128/128 [01:02<00:00]
Analyzing Job Descriptions for Location Restrictions...
Phase 3 Complete: Vaporized 89 'Fake Remote' jobs.

State Manager: Blocked 0 duplicate/previously-seen jobs.
Final valid NEW jobs to save: 654

Excel file saved successfully: remote_companies_hiring_2026-06-01_1430.xlsx
```

---

## 📊 Understanding the Output

The output is a formatted `.xlsx` Excel file named `remote_companies_hiring_YYYY-MM-DD_HHMM.xlsx`.

| Column | Description |
|---|---|
| **Company Name** | The hiring company |
| **Job Title** | The role being advertised |
| **Location** | Source and location tag (e.g., `Remotive: Worldwide`) |
| **Job URL** | Direct link to the job listing |
| **Date Posted** | When the job was posted |
| **Site** | Which platform the listing was found on |
| **Company Industry** | Industry/sector of the company |
| **Company Employee Count** | Headcount (if available) |
| **Salary Min** | Minimum salary (if listed) |
| **Salary Max** | Maximum salary (if listed) |
| **Remote Score** | The remote-friendliness score (higher = more global) |
| **Remote Status** | `Verified Worldwide` / `Open Worldwide` / `Likely Restricted` |

The output is **sorted by Remote Score (descending)** so the most globally-open companies appear first.

---

## 🤝 Contributing

Contributions are welcome and encouraged! Here are some ways you can help:

- 🐛 **Report bugs** — Open an issue describing what went wrong
- 🌐 **Add new job sources** — Submit a PR with a new scraper module
- 🧠 **Improve the filter engine** — Add smarter red/green flag patterns
- 📖 **Improve documentation** — Fix typos, add examples, translate

### How to Contribute

1. **Fork** this repository
2. **Create a feature branch**: `git checkout -b feature/add-new-board`
3. **Commit your changes**: `git commit -m "feat: add JobsCollider scraper"`
4. **Push your branch**: `git push origin feature/add-new-board`
5. **Open a Pull Request** — describe what you added and why

### Code Style

- Keep new scraper modules self-contained in their own file
- Follow the existing job dict schema (see [Add New Remote Job Boards](#add-new-remote-job-boards))
- Handle all exceptions gracefully — the scraper should never crash due to one bad source

---

## ⚠️ Disclaimer

This tool is intended for **personal, non-commercial use** to assist in your own job search. Please respect the terms of service of all platforms being scraped. The use of DuckDuckGo search dorking is used purely to discover publicly indexed job listings.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

You are free to use, modify, and distribute this project for any purpose.

---

<p align="center">
  Built with ❤️ to help developers find truly remote work worldwide.
  <br/>
  If this helped you land a job, consider giving it a ⭐
</p>
