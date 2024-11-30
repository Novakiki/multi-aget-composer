import pytest
from unittest.mock import AsyncMock
from cognitive_agents.memory.question_evolution import QuestionEvolution
from termcolor import colored

@pytest.mark.asyncio
class TestQuestionEvolution:
    @pytest.fixture
    async def evolution(self):
        """Create test evolution system."""
        # Create mocks
        mock_store = AsyncMock()
        mock_store.store_pattern.return_value = "test_pattern_1"
        
        mock_network = AsyncMock()
        
        mock_semantics = AsyncMock()
        mock_semantics.find_similar.return_value = [
            {
                'id': 'similar_1',
                'score': 0.9,
                'metadata': {
                    'content': 'How do patterns form?',
                    'themes': ['learning', 'patterns']
                }
            }
        ]
        
        mock_theme_extractor = AsyncMock()
        mock_theme_extractor.extract_themes.return_value = [
            'learning', 'evolution', 'patterns'
        ]
        
        return QuestionEvolution(
            store=mock_store,
            network=mock_network,
            semantics=mock_semantics,
            theme_extractor=mock_theme_extractor
        )
        
    async def test_question_evolution(self, evolution):
        """Test natural question evolution."""
        # Await the fixture first
        evolution = await evolution
        
        # Test question
        question = "How do patterns emerge naturally?"
        
        print(colored("\n🧠 Testing Question Evolution:", "cyan"))
        print(f"Question: {question}")
        
        # Let question evolve
        result = await evolution.evolve_question(question)
        
        # Verify evolution
        assert result['pattern_id'] == "test_pattern_1"
        assert len(result['connections']) > 0
        
        # Print evolution
        print(f"Pattern ID: {result['pattern_id']}")
        print(f"Similar Patterns: {len(result['connections'])}")