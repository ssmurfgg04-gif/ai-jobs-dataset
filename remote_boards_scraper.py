import requests
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET

def fetch_remotive_jobs(tech_skills):
    print("Scraping Remotive API...")
    url = "https://remotive.com/api/remote-jobs?category=software-dev"
    try:
        response = requests.get(url, timeout=15).json()
        jobs_data = response.get('jobs', [])
    except Exception as e:
        print(f"  -> Failed to fetch Remotive jobs: {e}")
        return []

    jobs = []
    for j in jobs_data:
        # Candidate Location filter
        location = j.get('candidate_required_location', '').lower()
        if not any(loc in location for loc in ['worldwide', 'india', 'anywhere', 'global']):
            continue
            
        # Tech filter (description or title)
        title = j.get('title', '').lower()
        desc = j.get('description', '').lower()
        if not any(skill in title or skill in desc for skill in tech_skills):
            continue

        jobs.append({
            'company': j.get('company_name', '')[:100],
            'title': j.get('title', '')[:100],
            'location': f"Remotive: {j.get('candidate_required_location', '')}",
            'job_url': j.get('url', ''),
            'date_posted': j.get('publication_date', '')[:10],
            'site': 'Remotive',
            'company_industry': 'Software Dev',
            'company_num_employees': None,
            'min_amount': None,
            'max_amount': None,
            'description': desc
        })
    return jobs

def fetch_remoteok_jobs(tech_skills):
    print("Scraping RemoteOK API...")
    url = "https://remoteok.com/api"
    # RemoteOK requires a realistic user-agent to not block the request
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers, timeout=15).json()
        jobs_data = response[1:] if len(response) > 1 else []
    except Exception as e:
        print(f"  -> Failed to fetch RemoteOK jobs: {e}")
        return []

    jobs = []
    for j in jobs_data:
        location = str(j.get('location', '')).lower()
        if not any(loc in location for loc in ['worldwide', 'india', 'anywhere', 'global']):
            continue
            
        title = str(j.get('position', '')).lower()
        company = str(j.get('company', ''))
        desc = str(j.get('description', '')).lower()
        tags = [str(t).lower() for t in j.get('tags', [])]
        
        # Check against tech_skills
        combined_text = title + " " + desc + " " + " ".join(tags)
        if not any(skill in combined_text for skill in tech_skills):
            continue

        jobs.append({
            'company': company[:100],
            'title': j.get('position', '')[:100],
            'location': f"RemoteOK: {j.get('location', '')}",
            'job_url': j.get('apply_url', j.get('url', '')),
            'date_posted': str(j.get('date', ''))[:10],
            'site': 'RemoteOK',
            'company_industry': 'Tech',
            'company_num_employees': None,
            'min_amount': j.get('salary_min', None),
            'max_amount': j.get('salary_max', None),
            'description': desc
        })
    return jobs

def fetch_weworkremotely_jobs(tech_skills):
    print("Scraping WeWorkRemotely RSS feed...")
    url = "https://weworkremotely.com/categories/remote-programming-jobs.rss"
    try:
        response = requests.get(url, timeout=15)
        root = ET.fromstring(response.content)
    except Exception as e:
        print(f"  -> Failed to fetch WWR RSS: {e}")
        return []

    jobs = []
    for item in root.findall('./channel/item'):
        title_text = item.find('title').text if item.find('title') is not None else ''
        desc_text = item.find('description').text if item.find('description') is not None else ''
        link = item.find('link').text if item.find('link') is not None else ''
        pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
        
        parts = title_text.split(': ', 1)
        company_name = parts[0] if len(parts) > 1 else "Unknown WWR Company"
        job_title = parts[1] if len(parts) > 1 else title_text

        text_lower = title_text.lower() + " " + desc_text.lower()
        
        # WWR specific checks for global scope
        is_remote = any(kw in text_lower for kw in ['anywhere in the world', 'worldwide', 'global', 'india'])
        if not is_remote:
            continue
            
        if not any(skill in text_lower for skill in tech_skills):
            continue

        jobs.append({
            'company': company_name[:100],
            'title': job_title[:100],
            'location': 'WWR: Worldwide/Anywhere',
            'job_url': link,
            'date_posted': pub_date,
            'site': 'WeWorkRemotely',
            'company_industry': 'Tech',
            'company_num_employees': None,
            'min_amount': None,
            'max_amount': None,
            'description': desc_text
        })
    return jobs

def fetch_remote_boards(search_terms):
    print("--- Starting Phase 2: Remote Niche Job Boards ---")
    tech_skills = search_terms
    
    all_jobs = []
    
    # 1. Remotive
    rem_jobs = fetch_remotive_jobs(tech_skills)
    if rem_jobs: all_jobs.extend(rem_jobs)
    
    # 2. RemoteOK
    rok_jobs = fetch_remoteok_jobs(tech_skills)
    if rok_jobs: all_jobs.extend(rok_jobs)
    
    # 3. WeWorkRemotely
    wwr_jobs = fetch_weworkremotely_jobs(tech_skills)
    if wwr_jobs: all_jobs.extend(wwr_jobs)
    
    df = pd.DataFrame(all_jobs)
    if not df.empty and 'job_url' in df.columns:
        df = df.drop_duplicates(subset=['job_url'])
        
    print(f"Phase 2 Complete: Scraped {len(df) if not df.empty else 0} matching jobs from Remote Boards.")
    return df
