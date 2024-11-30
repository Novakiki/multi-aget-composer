# Create a simple verification script
import sys
from termcolor import colored

def main():
    try:
        from tests.integration.neo4j.test_helpers import verify_neo4j_connection
        print(colored("\nTesting Neo4j Connection...", "cyan"))
        result = verify_neo4j_connection()
        print(colored(f"\nConnection Result: {result}", "green" if result else "red"))
    except Exception as e:
        print(colored(f"Error: {str(e)}", "red"))
        sys.exit(1)

if __name__ == "__main__":
    main() 