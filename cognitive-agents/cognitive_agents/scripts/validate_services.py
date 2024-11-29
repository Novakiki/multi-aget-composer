import os
from termcolor import colored
from pinecone import Pinecone

def validate_pinecone():
    """Validate Pinecone connection."""
    try:
        print(colored("\n🔍 Checking Pinecone Configuration:", "cyan"))
        
        # Check environment variables
        api_key = os.getenv('PINECONE_API_KEY')
        if not api_key:
            print(colored("❌ PINECONE_API_KEY not set", "red"))
            return False
            
        # Try connection
        pc = Pinecone(api_key=api_key)
        indexes = pc.list_indexes().names()
        print(colored(f"✅ Connected to Pinecone", "green"))
        print(f"  • Available Indexes: {indexes}")
        return True
        
    except Exception as e:
        print(colored(f"❌ Pinecone Error: {str(e)}", "red"))
        return False

if __name__ == "__main__":
    validate_pinecone() 