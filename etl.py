import os
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Google Sheets Connection
def connect_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(os.getenv("SHEET_NAME")).sheet1 # Assumes data is in first tab
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# Connect to NeonDB
def connect_db():
    db_string = os.getenv("DATABASE_URL")
    # SQLAlchemy requires 'postgresql://' not 'postgres://' usually
    if db_string.startswith("postgres://"):
        db_string = db_string.replace("postgres://", "postgresql://", 1)
    engine = create_engine(db_string)
    return engine

def transform_data(df):
    print("--- Starting Transformation ---")
    
    # 1. Data Cleaning: Drop duplicates based on Email
    initial_count = len(df)
    df = df.drop_duplicates(subset=['Email'])
    print(f"Removed {initial_count - len(df)} duplicate rows.")

    # 2. Handle Missing Values (Example: Default Department)
    df['Department'] = df['Department'].fillna('General')
    
    # 3. Validation: Ensure Email is valid (simple check)
    df = df[df['Email'].str.contains("@", na=False)]
    
    return df

def load_data(df, engine):
    print("--- Starting Loading ---")
    
    with engine.connect() as conn:
        for index, row in df.iterrows():
            try:
                # 1. Insert/Get Department ID
                # We use specific SQL queries to handle relations dynamically
                result = conn.execute(text("SELECT DepartmentID FROM Departments WHERE Name = :name"), {"name": row['Department']})
                dept_id = result.scalar()
                
                if not dept_id:
                    result = conn.execute(text("INSERT INTO Departments (Name) VALUES (:name) RETURNING DepartmentID"), {"name": row['Department']})
                    dept_id = result.scalar()
                    conn.commit() # Commit needed for the ID to be available immediately
                
                # 2. Insert Student
                # Using ON CONFLICT DO NOTHING to skip existing students (Idempotency)
                conn.execute(text("""
                    INSERT INTO Students (FullName, Email, EnrollmentYear, DepartmentID)
                    VALUES (:name, :email, :year, :dept_id)
                    ON CONFLICT (Email) DO NOTHING
                """), {
                    "name": row['Name'],
                    "email": row['Email'],
                    "year": row['EnrollmentYear'],
                    "dept_id": dept_id
                })
                conn.commit()
                print(f"Processed: {row['Name']}")
                
            except Exception as e:
                print(f"Error processing row {index}: {e}")

if __name__ == "__main__":
    # 1. Extract
    print("Extracting from Google Sheets...")
    df_raw = connect_sheets()
    
    # 2. Transform
    df_clean = transform_data(df_raw)
    
    # 3. Load
    engine = connect_db()
    load_data(df_clean, engine)
    print("ETL Job Complete.")