# config.py
# Environment configuration
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "../db")
    MEMORY_PATH = os.getenv("MEMORY_PATH", "../memory")
    # Add more environment variables as needed

settings = Settings()
