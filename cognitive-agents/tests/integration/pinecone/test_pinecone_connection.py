import os
import pytest
from pinecone import Pinecone

@pytest.mark.integration
def test_pinecone_connection():
    """Test basic Pinecone connection."""
    try:
        # Connect to Pinecone
        pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
        
        # List indexes
        indexes = pc.list_indexes()
        
        # Print info
        print("\n✨ Pinecone Connection:")
        print(f"Available Indexes: {indexes.names()}")
        
        assert len(indexes.names()) >= 0
        print("✅ Pinecone connection successful")
        
    except Exception as e:
        print(f"❌ Pinecone Error: {str(e)}")
        raise 