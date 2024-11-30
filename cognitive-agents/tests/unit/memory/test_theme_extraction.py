import pytest
from unittest.mock import AsyncMock
from cognitive_agents.memory.theme_extraction import ThemeExtraction

@pytest.mark.asyncio
class TestThemeExtraction:
    @pytest.fixture
    async def extractor(self):
        """Create test theme extractor."""
        mock_store = AsyncMock()
        mock_store.find_patterns_by_content.return_value = [
            {'themes': ['patterns', 'emergence']},
            {'themes': ['learning', 'evolution']}
        ]
        
        return ThemeExtraction(
            store=mock_store,
            network=AsyncMock()
        )
        
    async def test_theme_extraction(self, extractor):
        """Test natural theme extraction."""
        extractor = await extractor
        
        content = "How do patterns emerge and evolve?"
        themes = await extractor.extract_themes(content)
        
        assert 'patterns' in themes
        assert 'evolution' in themes
        assert len(themes) > 2  # Should find multiple themes 