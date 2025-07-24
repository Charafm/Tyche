from neo4j import GraphDatabase
from core.settings import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def test_connection():
    with driver.session() as sess:
        result = sess.run("RETURN 1 AS test")
        print(result.single()["test"])

if __name__ == "__main__":
    test_connection()
