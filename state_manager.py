import sqlite3
import hashlib

DB_FILE = "jobs_state.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Create table if not exists with Job URL (or hash) as primary key
    c.execute('''
        CREATE TABLE IF NOT EXISTS seen_jobs (
            job_hash TEXT PRIMARY KEY,
            job_url TEXT,
            company TEXT,
            title TEXT,
            date_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def generate_job_hash(url, company, title):
    # Sometimes URLs are empty or have tracking tags. We hash URL, or fallback to Company+Title
    unique_string = str(url).strip()
    if not unique_string or unique_string.lower() == 'nan':
        unique_string = f"{str(company).strip()}_{str(title).strip()}"
    return hashlib.md5(unique_string.encode('utf-8')).hexdigest()

def filter_new_jobs(df):
    if df.empty:
        return df
        
    init_db()
    conn = sqlite3.connect(DB_FILE)
    
    new_jobs_mask = []
    new_records = []
    
    for _, row in df.iterrows():
        j_hash = generate_job_hash(row.get('Job URL'), row.get('Company Name'), row.get('Job Title'))
        
        c = conn.cursor()
        c.execute("SELECT 1 FROM seen_jobs WHERE job_hash = ?", (j_hash,))
        if c.fetchone():
            new_jobs_mask.append(False)
        else:
            new_jobs_mask.append(True)
            new_records.append((j_hash, str(row.get('Job URL')), str(row.get('Company Name')), str(row.get('Job Title'))))
            
    # Memorize newly seen jobs
    if new_records:
        c = conn.cursor()
        c.executemany("INSERT INTO seen_jobs (job_hash, job_url, company, title) VALUES (?, ?, ?, ?)", new_records)
        conn.commit()
        
    conn.close()
    
    return df[new_jobs_mask].reset_index(drop=True)
