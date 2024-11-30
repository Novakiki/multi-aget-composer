import os
import pytest
from pinecone import Pinecone

@pytest.mark.integration
def test_pinecone_query():
    """Test Pinecone query operations."""
    try:
        # Connect to Pinecone
        pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
        index = pc.Index('virtual-limit-interactions')
        
        # Query test
        test_vector = [0.1] * 384
        results = index.query(
            vector=test_vector,
            top_k=5,
            include_metadata=True
        )
        
        print("\n✨ Query Results:")
        print(f"Found {len(results.matches)} matches")
        for match in results.matches:
            print(f"  • {match.metadata['content']} (score: {match.score:.2f})")
            
        assert len(results.matches) > 0
        
    except Exception as e:
        print(f"❌ Pinecone Error: {str(e)}")
        raise 