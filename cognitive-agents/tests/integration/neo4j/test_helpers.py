import subprocess
from termcolor import colored

def verify_neo4j_connection():
    """Verify Neo4j connection using cypher-shell."""
    try:
        # Use cypher-shell to test connection
        result = subprocess.run([
            'cypher-shell', 
            '-u', 'neo4j',
            '-p', 'evolution',
            'RETURN 1;'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(colored("✅ Neo4j connection verified", "green"))
            return True
        else:
            print(colored(f"❌ Neo4j connection failed: {result.stderr}", "red"))
            return False
    except Exception as e:
        print(colored(f"❌ Connection error: {str(e)}", "red"))
        return False 