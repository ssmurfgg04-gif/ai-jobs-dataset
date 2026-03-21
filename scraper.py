import subprocess
import sys
import os
import time
import random

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*dict.*")
warnings.filterwarnings("ignore", message=".*Pydantic.*")

def install_dependencies():
    packages = {
        "pandas": "pandas",
        "jobspy": "python-jobspy",
        "openpyxl": "openpyxl",
        "bs4": "beautifulsoup4",
        "duckduckgo_search": "duckduckgo-search",
        "tqdm": "tqdm"
    }
    missing = []
    for module_name, pip_name in packages.items():
        try:
            __import__(module_name)
        except ImportError:
            missing.append(pip_name)
            
    if missing:
        print(f"Installing missing dependencies: {', '.join(missing)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing, "--quiet"])

# Ensure everything is installed before continuing
install_dependencies()

import pandas as pd
from jobspy import scrape_jobs
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from hn_scraper import fetch_hn_jobs
from twitter_scraper import fetch_twitter_jobs
from remote_boards_scraper import fetch_remote_boards
from ats_scraper import fetch_ats_jobs
import json
from true_remote_filter import filter_true_remote
from state_manager import filter_new_jobs

# Load centralized config
with open("config.json", "r") as f:
    config = json.load(f)

SEARCH_TERMS = config.get("search_terms", [])
TECH_SKILLS = config.get("tech_skills", [])
PLATFORMS = config.get("jobspy_platforms", ["linkedin", "indeed"])
TARGET_LOCATIONS = config.get("jobspy_target_locations", ["USA", "Europe", "UK"])
RESULTS_WANTED = config.get("jobspy_results_wanted", 150)
HOURS_OLD = config.get("jobspy_hours_old", 720)

def main():
    all_data = []
    total_raw_results = 0

    print("--- Starting job scraping process ---")

    # ----------------------------------------------------
    # PHASE 1: Startup & Direct Sources (X & HackerNews)
    # ----------------------------------------------------
    try:
        hn_df = fetch_hn_jobs(TECH_SKILLS)
        if hn_df is not None and not hn_df.empty:
            all_data.append(hn_df)
            total_raw_results += len(hn_df)
    except Exception as e:
        print(f"Warning: Failed to scrape HackerNews. Error: {e}")

    try:
        tw_df = fetch_twitter_jobs(TECH_SKILLS)
        if tw_df is not None and not tw_df.empty:
            all_data.append(tw_df)
            total_raw_results += len(tw_df)
    except Exception as e:
        print(f"Warning: Failed to scrape X/Twitter. Error: {e}")

    # ----------------------------------------------------
    # PHASE 2: Remote Niche Job Boards
    # ----------------------------------------------------
    try:
        boards_df = fetch_remote_boards(TECH_SKILLS)
        if boards_df is not None and not boards_df.empty:
            all_data.append(boards_df)
            total_raw_results += len(boards_df)
    except Exception as e:
        print(f"Warning: Failed to scrape Remote Niche Boards. Error: {e}")

    # ----------------------------------------------------
    # PHASE 4: Mainstream/MNC ATS Direct Platforms
    # ----------------------------------------------------
    try:
        ats_df = fetch_ats_jobs(TECH_SKILLS)
        if ats_df is not None and not ats_df.empty:
            all_data.append(ats_df)
            total_raw_results += len(ats_df)
    except Exception as e:
        print(f"Warning: Failed to scrape ATS Platforms. Error: {e}")

    # ----------------------------------------------------
    # MAINSTREAM BOARDS (LinkedIn, Indeed, Glassdoor)
    # ----------------------------------------------------
    for loc in TARGET_LOCATIONS:
        for term in SEARCH_TERMS:
            for platform in PLATFORMS:
                print(f"Scraping {platform} for '{term}' in '{loc}'...")
                try:
                    kwargs = {
                        "site_name": [platform],
                        "search_term": term,
                        "location": loc,
                        "results_wanted": RESULTS_WANTED,
                        "is_remote": True,
                        "hours_old": HOURS_OLD
                    }
                    # Indeed requires exact country enums if we supply them
                    if platform == "indeed" and loc.lower() in ["usa", "uk", "canada"]:
                        kwargs["country_indeed"] = loc.lower()
                    
                    jobs = scrape_jobs(**kwargs)
                    
                    count = len(jobs) if jobs is not None and not jobs.empty else 0
                    print(f"Scraped {count} results from {platform}")
                    
                    if count > 0:
                        all_data.append(jobs)
                        total_raw_results += count

                except Exception as e:
                    print(f"Warning: Failed to scrape {platform} for '{term}' in '{loc}'. Error: {e}")

                sleep_t = random.uniform(3, 7)
                time.sleep(sleep_t)

    print(f"\nTotal raw results collected: {total_raw_results}")

    if total_raw_results < 100:
        print("Warning: Total results collected are less than 100. Please re-run the script or check your internet connection.")

    if not all_data:
        print("No data collected across any platform. Exiting.")
        return

    # Merge all datasets into one DataFrame
    df = pd.concat(all_data, ignore_index=True)

    # 1. Map columns securely
    COLUMNS_TO_KEEP = {
        'company': 'Company Name',
        'title': 'Job Title',
        'location': 'Location',
        'job_url': 'Job URL',
        'date_posted': 'Date Posted',
        'site': 'Site',
        'company_industry': 'Company Industry',
        'company_num_employees': 'Company Employee Count',
        'min_amount': 'Salary Min',
        'max_amount': 'Salary Max',
        'description': 'Description'
    }

    # Add any gracefully missing columns to ensure uniform shape
    for col in COLUMNS_TO_KEEP.keys():
        if col not in df.columns:
            df[col] = None

    # Keep only target columns
    df = df[list(COLUMNS_TO_KEEP.keys())]
    
    # Rename to clean labels
    df.rename(columns=COLUMNS_TO_KEEP, inplace=True)

    # 2. Filter out rows where Company Name is null or empty
    df['Company Name'] = df['Company Name'].fillna("").astype(str)
    df = df[df['Company Name'].str.strip() != ""]
    df = df[df['Company Name'].str.strip().str.lower() != "nan"]
    df = df[df['Company Name'].str.strip().str.lower() != "none"]
    
    # Create an invisible column for highly accurate deduplication
    df['Company_Clean'] = df['Company Name'].str.strip().str.lower()

    # 3. Drop duplicate rows based on company name
    df = df.drop_duplicates(subset=['Company_Clean'], keep='first')
    df.drop(columns=['Company_Clean'], inplace=True)

    # 4. Reset index
    df = df.reset_index(drop=True)

    # 5. Sort final dataframe alphabetically by Company Name
    df = df.sort_values(by='Company Name', ascending=True)

    # 6. Print total unique companies
    unique_companies = len(df)
    print(f"After deduplication: {unique_companies} unique companies")

    # ----------------------------------------------------
    # PHASE 3: TRUE REMOTE FILTER ENGINE
    # ----------------------------------------------------
    df = filter_true_remote(df)
    
    # ----------------------------------------------------
    # STATE MANAGER: REMOVE PREVIOUSLY SEEN JOBS
    # ----------------------------------------------------
    original_size = len(df)
    df = filter_new_jobs(df)
    print(f"State Manager: Blocked {original_size - len(df)} duplicate/previously-seen jobs.")
    
    print(f"Final valid NEW jobs to save: {len(df)}")

    # Proceed to format output Excel spreadsheet
    from datetime import datetime
    date_str = datetime.now().strftime("%Y-%m-%d_%H%M")
    filename = f"remote_companies_hiring_{date_str}.xlsx"
    try:
        # Strip tz-awareness from dates as openpyxl doesn't support them well
        if 'Date Posted' in df.columns:
            try:
                df['Date Posted'] = pd.to_datetime(df['Date Posted']).dt.tz_localize(None)
            except:
                pass

        # Perform the basic save
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Companies Hiring Remote")

        # Reopen workbook for targeted formatting
        wb = openpyxl.load_workbook(filename)
        ws = wb["Companies Hiring Remote"]

        # Color definitions
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
        alt_fill = PatternFill(start_color="DEEAF1", end_color="DEEAF1", fill_type="solid")

        # 7. Apply Header styles
        for cell in ws[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center", vertical="center")

        # 8. Apple Alternate row coloring
        for row_idx, row in enumerate(ws.iter_rows(min_row=2, max_row=ws.max_row), start=2):
            if row_idx % 2 == 0:
                for cell in row:
                    cell.fill = alt_fill

        # 9. Auto-fit all column widths based on content
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                val_str = str(cell.value) if cell.value else ""
                max_length = max(max_length, len(val_str))
            
            # Use max length, capping it so it doesn't get ridiculously large
            ws.column_dimensions[column].width = min(max_length + 2, 80)

        # 10. Freeze the top header row
        ws.freeze_panes = "A2"
        
        # 11. Add a basic filter on all columns
        ws.auto_filter.ref = ws.dimensions

        # Resave formatted output
        wb.save(filename)
        print(f"Excel file saved successfully: {filename}")
        
    except Exception as e:
        print(f"Warning: Failed to save or format the Excel file. Error: {e}")

if __name__ == "__main__":
    main()
