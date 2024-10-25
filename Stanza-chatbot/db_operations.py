# db_operations.py
from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASS

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

def run_query(query):
    try:    
        with driver.session() as session:
            session = driver.session()
            result = session.run(query)
            return list(result)  
           
    except Exception as e:
        print(f"Veritabanı hatası: {e}")
        return []


def close_connection():
    driver.close()
