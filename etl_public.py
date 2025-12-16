import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

def load_public_data():
    # 1. Extract
    df = pd.read_csv('public_data.csv')
    print("Extracted CSV Data...")

    # 2. Connect
    db_string = os.getenv("DATABASE_URL")
    if db_string.startswith("postgres://"):
        db_string = db_string.replace("postgres://", "postgresql://", 1)
    engine = create_engine(db_string)

    # 3. Load (Auto-create table 'products')
    df.to_sql('products', engine, if_exists='replace', index=False)
    print(" Public Dataset Loaded into NeonDB!")

if __name__ == "__main__":
    load_public_data()