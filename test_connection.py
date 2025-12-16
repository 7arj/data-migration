import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# environment variables
load_dotenv()

def test_db_connection():
    try:
       
        db_string = os.getenv("DATABASE_URL")
        
        # SQLAlchemy fix for neon connection string
        if db_string.startswith("postgres://"):
            db_string = db_string.replace("postgres://", "postgresql://", 1)
            
        # Create engine and connect
        engine = create_engine(db_string)
        
        with engine.connect() as connection:
            
            result = connection.execute(text("SELECT 1"))
            
            print("Connected to NeonDB") 
            print("Database connection successful.")

    except Exception as e:
        print(f"Connection Failed: {e}")

if __name__ == "__main__":
    test_db_connection()