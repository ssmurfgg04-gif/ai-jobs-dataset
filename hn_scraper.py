import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

def fetch_hn_jobs(search_terms, max_jobs=2000):
    print("Scraping HackerNews: Who is Hiring...")
    user_url = "https://hacker-news.firebaseio.com/v0/user/whoishiring.json"
    
    try:
        user_data = requests.get(user_url).json()
        submissions = user_data.get('submitted', [])
    except Exception as e:
        print(f"Failed to fetch HN user data: {e}")
        return pd.DataFrame()

    target_post_id = None
    for item_id in submissions[:15]:
        try:
            item_data = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json").json()
            if item_data and "title" in item_data and "Ask HN: Who is hiring?" in item_data['title']:
                target_post_id = item_id
                break
        except Exception:
            pass

    if not target_post_id:
        print("Could not find the most recent 'Who is hiring' post.")
        return pd.DataFrame()

    print(f"Found 'Who is Hiring' post ID {target_post_id}. Fetching comments...")
    
    try:
        post_data = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{target_post_id}.json").json()
        comment_ids = post_data.get('kids', [])
    except Exception as e:
        print(f"Failed to fetch HN post kids: {e}")
        return pd.DataFrame()
    
    jobs = []
    
    import concurrent.futures
    from tqdm import tqdm

    def parse_comment(c_id):
        try:
            c_data = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{c_id}.json").json()
            if not c_data or c_data.get('type') != 'comment' or c_data.get('deleted'):
                return None
                
            text = c_data.get('text', '')
            if not text:
                return None
                
            text_lower = text.lower()
            
            # Simple keyword matching: Must be remote/india/worldwide
            is_remote = any(kw in text_lower for kw in ['remote', 'india', 'worldwide', 'anywhere', 'global'])
            if not is_remote:
                return None
                
            # Filter by matching any of our required tech stacks
            if not any(skill in text_lower for skill in search_terms):
                return None
                
            # Parse HTML text safely
            soup = BeautifulSoup(text, 'html.parser')
            clean_text = soup.get_text(separator=' ').strip()
            lines = clean_text.split('\n')
            first_line = lines[0].strip() if lines else "HN Startup Job"
            
            # Extract basic info, HN format depends on pipe dividers usually
            parts = [p.strip() for p in first_line.split('|')]
            company_name = parts[0] if len(parts) > 0 else "HN Startup"
            job_title = parts[1] if len(parts) > 1 else first_line[:100]
            date_posted = datetime.fromtimestamp(c_data.get('time', 0)) if c_data.get('time') else datetime.now()
            
            return {
                'Company Name': company_name[:100],
                'Job Title': job_title[:100],
                'Location': 'Remote / HN',
                'Job URL': f"https://news.ycombinator.com/item?id={c_id}",
                'Date Posted': date_posted,
                'Site': 'HackerNews',
                'Company Industry': 'Startup (HN)',
                'Company Employee Count': None,
                'Salary Min': None,
                'Salary Max': None
            }
            
        except Exception:
            return None

    # Fetch comments concurrently to vastly improve performance
    print("Processing comments...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(tqdm(executor.map(parse_comment, comment_ids[:max_jobs]), total=min(len(comment_ids), max_jobs), desc="Parsing HackerNews", unit="cmt"))
        
    for res in results:
        if res:
            jobs.append(res)
            
    df = pd.DataFrame(jobs)
    total_found = len(df) if not df.empty else 0
    print(f"Scraped {total_found} matching HackerNews jobs.")
    return df
