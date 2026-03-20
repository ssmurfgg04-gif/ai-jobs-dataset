import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import concurrent.futures
from tqdm import tqdm

RED_FLAGS = [
    r'\bus\b only',
    r'\bunited states\b only',
    r'must reside in (?:the )?us',
    r'no visa sponsorship',
    r'us citizen',
    r'w2 only',
    r'w-2 only',
    r'citizenship required',
    r'cleared candidates',
    r'security clearance',
    r'uk only',
    r'europe only',
    r'must live in (?:the )?(?:us|uk|eu)'
]

GREEN_FLAGS = [
    r'work from anywhere',
    r'anywhere in the world',
    r'global team',
    r'worldwide',
    r'remote india',
    r'remote - india',
    r'overlap with',
    r'distributed team',
    r'digital nomad'
]

def analyze_description(text):
    if not text or not isinstance(text, str):
        return 0, 'Unknown'
        
    text_lower = text.lower()
    score = 0
    status = 'Open Worldwide'
    
    for flag in RED_FLAGS:
        if re.search(flag, text_lower):
            score -= 10
            status = 'Likely Restricted (US/EU Only)'
            
    for flag in GREEN_FLAGS:
        if re.search(flag, text_lower):
            score += 5
            status = 'Verified Worldwide'
            
    return score, status

def fetch_text_from_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        # naive text extraction
        return soup.get_text(separator=' ', strip=True)
    except Exception:
        return ""

def filter_true_remote(df):
    print("\n--- Starting Phase 3: True Remote Filtering Engine ---")
    if df.empty:
        return df

    # We need a Description column
    if 'Description' not in df.columns:
        df['Description'] = ""

    # Ensure Description is text
    df['Description'] = df['Description'].fillna("").astype(str)

    # For those missing descriptions, try a quick scrape
    missing_desc_mask = df['Description'].str.strip() == ""
    urls_to_scrape = df.loc[missing_desc_mask, 'Job URL'].tolist()
    
    if urls_to_scrape:
        print(f"Fetching deeper job descriptions for {len(urls_to_scrape)} raw links...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            fetched_texts = list(tqdm(executor.map(fetch_text_from_url, urls_to_scrape), total=len(urls_to_scrape), desc="Downloading Missing JDs", unit="page"))
            
        df.loc[missing_desc_mask, 'Description'] = fetched_texts

    print("Analyzing Job Descriptions for Location Restrictions (US Only vs Global)...")
    
    scores = []
    statuses = []
    for desc in tqdm(df['Description'], desc="NLP Parsing", unit="job"):
        score, status = analyze_description(desc)
        scores.append(score)
        statuses.append(status)
        
    df['Remote Score'] = scores
    df['Remote Status'] = statuses
    
    # Filter out strongly restricted "Fake Remote" jobs (US/EU specific)
    original_count = len(df)
    df = df[df['Remote Score'] > -5] 
    filtered_count = len(df)
    
    print(f"Phase 3 Complete: Vaporized {original_count - filtered_count} 'Fake Remote' jobs.")
    
    # Clean up massive text column before exporting to excel
    if 'Description' in df.columns:
        df = df.drop(columns=['Description'])
        
    # Sort so 'Verified Worldwide' is at the top
    df = df.sort_values(by=['Remote Score', 'Company Name'], ascending=[False, True])
    
    # Reset index cleanly
    df = df.reset_index(drop=True)
    
    return df
