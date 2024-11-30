import os
import pytest
from pinecone import Pinecone, ServerlessSpec

@pytest.mark.integration
def test_pinecone_index():
    """Test Pinecone index creation and usage."""
    try:
        # Connect to Pinecone
        pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
        
        # Index name
        index_name = 'virtual-limit-interactions'
        
        # Create index if it doesn't exist
        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=384,
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='gcp',
                    region='us-west-2'  # Use your region
                )
            )
            print(f"\n✨ Created index: {index_name}")
        
        # Get index
        index = pc.Index(index_name)
        
        # Test vector
        test_vector = [0.1] * 384
        
        # Upsert test data
        index.upsert([
            ('test_1', test_vector, {'content': 'Test pattern'})
        ])
        
        print("✅ Index operations successful")
        
    except Exception as e:
        print(f"❌ Pinecone Error: {str(e)}")
        raise 