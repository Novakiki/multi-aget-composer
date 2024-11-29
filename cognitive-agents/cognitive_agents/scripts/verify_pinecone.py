import os
from pinecone import Pinecone
from termcolor import colored

def verify_pinecone():
    """Verify Pinecone connection."""
    try:
        pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
        indexes = pc.list_indexes().names()
        print(colored("✅ Pinecone Connected", "green"))
        print(f"  • Available Indexes: {indexes}")
    except Exception as e:
        print(colored(f"❌ Pinecone Error: {str(e)}", "red"))

if __name__ == "__main__":
    verify_pinecone() 