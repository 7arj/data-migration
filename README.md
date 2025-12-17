# Student Data Migration Project (Google Sheets → NeonDB)

##  Overview
This project is a fully automated ETL pipeline that extracts student data from Google Sheets, transforms/validates it using Python (Pandas), and loads it into a normalized PostgreSQL database hosted on NeonDB.

## Tech Stack
- **Source:** Google Sheets API
- **Destination:** NeonDB (PostgreSQL 15)
- **Language:** Python 3.10 (Pandas, SQLAlchemy)
- **Automation:** Google Apps Script (Javascript)

##  Project Structure
- `etl.py`: Main ETL script for Student Data.
- `etl_public.py`: Modular script for Public Dataset (CSV) ingestion.
- `schema.sql`: Database schema (3NF) creation script.
- `queries.sql`: Analytical SQL queries.
- `google_apps_script.js`: Validation logic for Google Sheets.

##  Setup & Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/7arj/data-migration.git
   cd data-migration
