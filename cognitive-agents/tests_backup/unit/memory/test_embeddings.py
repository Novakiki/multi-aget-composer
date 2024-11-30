import pytest
from cognitive_agents.memory.embeddings import EmbeddingGenerator
from termcolor import colored

@pytest.mark.asyncio
class TestEmbeddings:
    @pytest.fixture
    async def generator(self):
        """Create embedding generator."""
        return EmbeddingGenerator()
        
    async def test_embedding_generation(self, generator):
        """Test embedding generation."""
        # Await the fixture first
        generator = await generator
        
        # Test text
        text = "How do patterns emerge naturally?"
        
        print(colored("\n🧬 Testing Embeddings:", "cyan"))
        print(f"Text: {text}")
        
        # Generate embedding
        embedding = generator.generate(text)
        
        # Verify embedding
        assert len(embedding) == 384  # MiniLM model dimension
        print(f"Embedding Size: {len(embedding)}")
        print(f"First 5 Values: {embedding[:5]}")