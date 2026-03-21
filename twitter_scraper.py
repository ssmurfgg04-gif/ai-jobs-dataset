import pandas as pd
from duckduckgo_search import DDGS
from datetime import datetime
import time
from tqdm import tqdm

def fetch_twitter_jobs(search_terms, max_results=500):
    print("Scraping X/Twitter via DuckDuckGo Search (Dorking)...")
    jobs = []
    
    # Tech words to cycle queries
    queries = []
    for tech in search_terms:
        queries.append(f'site:x.com "hiring" ("remote" OR "anywhere" OR "worldwide" OR "india") "{tech}"')
        queries.append(f'site:twitter.com "hiring" ("remote" OR "anywhere" OR "worldwide" OR "india") "{tech}"')

    ddgs = DDGS()
    
    for idx, q in enumerate(tqdm(queries, desc="Querying Twitter/X", unit="search")):
        try:
            # Rate limits can apply, taking small steps
            results = list(ddgs.text(q, max_results=max_results // len(queries)))
            for r in results:
                title = r.get('title', '')
                body = r.get('body', '')
                href = r.get('href', '')
                
                if "status" not in href:
                    continue
                    
                company_name = title.split(' on X')[0].split(' on Twitter')[0].strip()
                
                # Loose validation
                if not any(kw in body.lower() or kw in title.lower() for kw in ['hiring', 'looking for', 'open role', 'join our team', 'job']):
                    continue

                jobs.append({
                    'company': company_name[:100],
                    'title': title[:100],
                    'location': 'Remote / X',
                    'job_url': href,
                    'date_posted': datetime.now(),
                    'site': 'X (Twitter)',
                    'company_industry': 'Tech/Web (X)',
                    'company_num_employees': None,
                    'min_amount': None,
                    'max_amount': None,
                    'description': body
                })
        except Exception as e:
            pass
            
        time.sleep(1) # Be gentle to search engine
            
    df = pd.DataFrame(jobs)
    if not df.empty and 'job_url' in df.columns:
        df = df.drop_duplicates(subset=['job_url'])
        
    total_found = len(df) if not df.empty else 0
    print(f"Scraped {total_found} matching X/Twitter jobs.")
    return df
