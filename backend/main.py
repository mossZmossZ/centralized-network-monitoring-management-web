import os
from dotenv import load_dotenv
from fastapi import FastAPI

# Load environment variables
load_dotenv()

# Read database credentials from .env
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!", "db_user": DB_USER, "db_name": DB_NAME}
