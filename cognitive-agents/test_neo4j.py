from neo4j import GraphDatabase
from termcolor import colored

# Test connection
def test_connection():
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(
        uri, 
        auth=("neo4j", "n3qG0pUxARSxU__eETM--a4Q39bW18yl0ZwZV12wpOU")
    )
    
    try:
        with driver.session() as session:
            result = session.run("RETURN 1")
            print(colored("✅ Connected to Neo4j!", "green"))
            print(colored("Current directory: " + session.run("CALL dbms.listConfig() YIELD name, value WHERE name='server.directories.data' RETURN value").single()['value'], "cyan"))
    except Exception as e:
        print(colored(f"❌ Connection failed: {e}", "red"))
    finally:
        driver.close()

if __name__ == "__main__":
    test_connection() 