import pytest
from cognitive_agents.agents.specialized_agents import CognitiveOrchestrator

@pytest.mark.asyncio
class TestOrchestrator:
    @pytest.fixture
    async def orchestrator(self):
        return CognitiveOrchestrator()
    
    async def test_single_thought(self, orchestrator):
        """Test single thought processing."""
        orchestrator = await orchestrator
        
        result = await orchestrator.process_thoughts(
            "Starting this project with mixed emotions"
        )
        assert "patterns" in result
        assert "emotions" in result
        assert "synthesis" in result
        
    async def test_batch_processing(self, orchestrator):
        """Test batch thought processing."""
        orchestrator = await orchestrator
        
        thoughts = [
            "Starting the project with careful planning",
            "Making progress through systematic steps",
            "Encountering challenges but staying focused"
        ]
        result = await orchestrator.process_thoughts(thoughts)
        assert "results" in result
        assert len(result["results"]) == len(thoughts)
        
    async def test_sequential_processing(self, orchestrator):
        """Test sequential processing (small batch)."""
        orchestrator = await orchestrator
        
        thoughts = ["First thought", "Second thought"]
        result = await orchestrator.process_thoughts(thoughts)
        assert "results" in result
        assert len(result["results"]) == 2 