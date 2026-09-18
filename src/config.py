import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv(
    "PINECONE_INDEX_NAME",
    "darukaa-biodiversity"
)

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set.")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is not set.")