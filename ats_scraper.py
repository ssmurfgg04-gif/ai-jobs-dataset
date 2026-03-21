import pandas as pd
from duckduckgo_search import DDGS
from datetime import datetime
import time
from tqdm import tqdm

def fetch_ats_jobs(search_terms, max_results=1000):
    print("Scraping top-tier ATS platforms (Greenhouse, Lever, Workable, Ashby)...")
    jobs = []
    
    platforms = [
        "boards.greenhouse.io",
        "jobs.lever.co",
        "apply.workable.com",
        "jobs.ashbyhq.com"
    ]
    
    queries = []
    
    for platform in platforms:
        for tech in search_terms:
            # Dork to find remote jobs open to India/Worldwide on these ATS platforms
            queries.append(f'site:{platform} "{tech}" ("remote" OR "anywhere" OR "worldwide" OR "india")')

    ddgs = DDGS()
    
    for idx, q in enumerate(tqdm(queries, desc="Searching ATS Platforms", unit="search")):
        try:
            results = list(ddgs.text(q, max_results=max_results // len(queries)))
            for r in results:
                title = r.get('title', '')
                body = r.get('body', '').lower()
                href = r.get('href', '')
                
                # Try to extract the company name neatly
                company_name = "Unknown ATS Company"
                if "greenhouse.io" in href:
                    company_name = href.split('/')[-2] if len(href.split('/')) > 3 else "Greenhouse Company"
                elif "lever.co" in href:
                    company_name = href.split('/')[-2] if len(href.split('/')) > 3 else "Lever Company"
                elif "workable.com" in href:
                    company_name = href.split('/')[-2] if len(href.split('/')) > 3 else "Workable Company"
                elif "ashbyhq.com" in href:
                     company_name = href.split('/')[-2] if len(href.split('/')) > 3 else "Ashby Company"
                     
                company_name = company_name.replace('-', ' ').title()

                jobs.append({
                    'company': company_name[:100],
                    'title': title[:100],
                    'location': 'Remote / ATS',
                    'job_url': href,
                    'date_posted': datetime.now(),
                    'site': 'ATS Platform',
                    'company_industry': 'Tech/MNC',
                    'company_num_employees': None,
                    'min_amount': None,
                    'max_amount': None,
                    'description': body
                })
        except Exception as e:
            pass
            
        time.sleep(1) # Be gentle to circumvent rate limits
            
    df = pd.DataFrame(jobs)
    if not df.empty and 'job_url' in df.columns:
        df = df.drop_duplicates(subset=['job_url'])
        
    total_found = len(df) if not df.empty else 0
    print(f"Phase 4 Complete: Scraped {total_found} global roles directly from ATS platforms.")
    return df
