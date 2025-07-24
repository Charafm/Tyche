import os
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
# KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
USE_VECTOR_STORE = os.getenv("USE_VECTOR_STORE", "faiss")
CHROMA_DIR = os.getenv("CHROMA_PERSIST_DIR", "chroma_db")
