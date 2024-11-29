import pytest
from cognitive_agents.agents.specialized_agents import CognitiveOrchestrator
from cognitive_agents.pattern_store.db import PatternStore
from pathlib import Path
from termcolor import colored

@pytest.mark.asyncio
class TestOrchestrator:
    """Test the core orchestration functionality."""
    
    @pytest.fixture(autouse=True, scope="class")
    def setup_db(self):
        """Setup fresh database before any tests."""
        # Delete existing DB
        db_path = Path(__file__).parent.parent / "cognitive_agents/pattern_store/patterns.db"
        if db_path.exists():
            db_path.unlink()
        
        # Let tests run
        yield
        
        # Cleanup after all tests
        if db_path.exists():
            db_path.unlink()
    
    @pytest.fixture(autouse=True)
    async def setup_cleanup(self):
        """Per-test cleanup."""
        store = PatternStore()
        
        # Run test
        yield
        
        # Clean tables between tests
        store.cleanup_sequences()  # Only clean sequences, keep structure
    
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
        
        try:
            result = await orchestrator.process_thoughts(thoughts)
            print(colored(f"\nBatch result: {result}", "cyan"))  # Debug
            
            assert "results" in result, "Missing 'results' key in response"
            assert isinstance(result["results"], list), "'results' should be a list"
            assert len(result["results"]) == len(thoughts), f"Expected {len(thoughts)} results, got {len(result['results'])}"
            
            # Check each result
            for i, res in enumerate(result["results"]):
                assert "patterns" in res, f"Result {i} missing patterns"
                assert "emotions" in res, f"Result {i} missing emotions"
                
        except Exception as e:
            print(colored(f"\n❌ Batch processing error: {str(e)}", "red"))
            raise
    
    async def test_sequential_processing(self, orchestrator):
        """Test sequential processing (small batch)."""
        orchestrator = await orchestrator
        
        thoughts = ["First thought", "Second thought"]
        result = await orchestrator.process_thoughts(thoughts)
        assert "results" in result
        assert len(result["results"]) == 2 