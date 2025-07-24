#!/usr/bin/env python3
import os
import textwrap

# Root of your project
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# Define folders to create
folders = [
    "core",
    "ingestion",
    "information_extraction",
    "entity_linking",
    "graph_store",
    "embeddings",
    "vector_index",
    "rag_api",
    "pipeline",
    "tests",
    "scripts"
]

# Files with optional boilerplate
files = {
    "requirements.txt": textwrap.dedent("""\
        spacy
        neo4j
        feedparser
        newspaper3k
        sentence-transformers
        faiss-cpu
        fastapi
        uvicorn
        llama-cpp-python
        pytest
        pyyaml
        loguru
    """),
    ".env.example": textwrap.dedent("""\
        # Copy this to .env and fill in your secrets
        NEO4J_URI=bolt://localhost:7687
        NEO4J_USER=neo4j
        NEO4J_PASSWORD=yourpassword
        KAFKA_BOOTSTRAP_SERVERS=localhost:9092
        FAISS_HOST=localhost
        FAISS_PORT=6000
    """),
    "docker-compose.yml": textwrap.dedent("""\
        version: "3.8"
        services:
          neo4j:
            image: neo4j:5-community
            ports: ["7474:7474","7687:7687"]
            environment:
              - NEO4J_AUTH=neo4j/yourpassword
          zookeeper:
            image: bitnami/zookeeper:latest
            ports: ["2181:2181"]
          kafka:
            image: bitnami/kafka:latest
            ports: ["9092:9092"]
            environment:
              - KAFKA_BROKER_ID=1
              - KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092
              - KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
          faiss-service:
            build: ./vector_index
            ports: ["6000:6000"]
        """),
    "README.md": "# Tyche\n\nScaffolded Tyche GraphRAG Finance Platform.\n",
    "core/settings.py": textwrap.dedent("""\
        import os
        from dotenv import load_dotenv

        load_dotenv()

        NEO4J_URI = os.getenv(\"NEO4J_URI\")
        NEO4J_USER = os.getenv(\"NEO4J_USER\")
        NEO4J_PASSWORD = os.getenv(\"NEO4J_PASSWORD\")
        KAFKA_BOOTSTRAP_SERVERS = os.getenv(\"KAFKA_BOOTSTRAP_SERVERS\")
        FAISS_HOST = os.getenv(\"FAISS_HOST\")
        FAISS_PORT = int(os.getenv(\"FAISS_PORT\", 6000))
    """),
    "core/utils.py": textwrap.dedent("""\
        def hello():
            print(\"Hello, Tyche!\")
    """),
    "ingestion/rss_fetcher.py": textwrap.dedent("""\
        from core.utils import hello

        if __name__ == \"__main__\":
            hello()
            print(\"RSS fetcher is up and running.\")
    """),
    "information_extraction/ner_spacy.py": textwrap.dedent("""\
        import spacy

        nlp = spacy.load(\"en_core_web_sm\")

        def extract_entities(text):
            doc = nlp(text)
            return [(ent.text, ent.label_) for ent in doc.ents]

        if __name__ == \"__main__\":
            sample = \"Apple acquired Beats for $3B in 2014.\"
            print(extract_entities(sample))
    """),
    "entity_linking/blink_client.py": "# placeholder for BLINK integration\n",
    "graph_store/neo4j_client.py": textwrap.dedent("""\
        from neo4j import GraphDatabase
        from core.settings import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

        def test_connection():
            with driver.session() as sess:
                result = sess.run(\"RETURN 1 AS test\")
                print(result.single()[\"test\"])

        if __name__ == \"__main__\":
            test_connection()
    """),
    "embeddings/sbert_embed.py": "# placeholder for SBERT embedding script\n",
    "vector_index/faiss_index.py": "# placeholder for FAISS index service\n",
    "rag_api/app.py": textwrap.dedent("""\
        from fastapi import FastAPI

        app = FastAPI()

        @app.get(\"/health\")
        def health():
            return {\"status\": \"ok\"}

        @app.get(\"/query\")
        def query(text: str):
            # placeholder for RAG query logic
            return {\"answer\": \"This is a stub.\"}
    """),
    "pipeline/run_ingest.py": "# placeholder for ingestion orchestration\n",
    "scripts/dev-setup.py": textwrap.dedent("""\
        import os
        # Here you can seed Neo4j or verify services
        print(\"Dev setup complete. Seed your data as needed.\")
    """),
    "tests/test_utils.py": textwrap.dedent("""\
        from core.utils import hello

        def test_hello(capsys):
            hello()
            captured = capsys.readouterr()
            assert \"Hello\" in captured.out
    """)
}

def main():
    # Create folders
    for f in folders:
        path = os.path.join(ROOT, f)
        os.makedirs(path, exist_ok=True)
        print(f"Created directory: {f}")

    # Create files
    for filepath, content in files.items():
        fullpath = os.path.join(ROOT, filepath)
        d = os.path.dirname(fullpath)
        if d and not os.path.exists(d):
            os.makedirs(d)
        with open(fullpath, "w", encoding="utf-8") as fp:
            fp.write(content)
        print(f"Created file: {filepath}")

    print("\nAll scaffolding complete! You can now:\n"
          "  1. Activate your venv\n"
          "  2. Install requirements\n"
          "  3. Copy .env.example to .env and fill in values\n"
          "  4. docker-compose up -d\n"
          "  5. Begin coding in each module as per the Tyche blueprint.")

if __name__ == "__main__":
    main()
