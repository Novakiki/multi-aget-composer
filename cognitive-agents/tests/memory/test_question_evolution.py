import pytest
from termcolor import colored
from cognitive_agents.memory.question_evolution import QuestionEvolution

@pytest.mark.asyncio
class TestQuestionEvolution:
    @pytest.fixture
    async def evolution(self):
        return QuestionEvolution()
        
    async def test_natural_resonance(self, evolution):
        """Test how questions naturally resonate."""
        evolution = await evolution
        
        # Individual question
        q1 = {
            'content': 'How do patterns emerge?',
            'intent': 'understanding',
            'context': 'learning'
        }
        
        # Related collective question
        q2 = {
            'content': 'What drives pattern formation?',
            'intent': 'exploration',
            'context': 'learning'
        }
        
        # Store questions
        evolution.space['questions']['individual'].append(q1)
        evolution.space['questions']['collective'].append(q2)
        
        # Observe new question
        new_question = {
            'content': 'Why do patterns evolve naturally?',
            'intent': 'understanding',
            'context': 'learning'
        }
        
        result = await evolution.observe_question(new_question)
        
        print(colored("\n🔍 Testing Natural Resonance:", "cyan"))
        print(f"New Question: {new_question['content']}")
        print(f"Found Patterns: {len(result.get('patterns', []))}")
        
        # Verify natural resonance
        assert len(result.get('patterns', [])) > 0
        assert any(p.get('resonance', 0) > 0.7 for p in result.get('patterns', [])) 
        
    async def test_evolution_path(self, evolution):
        """Test how questions naturally evolve."""
        evolution = await evolution
        
        # Create natural evolution path
        questions = [
            {
                'content': 'What is learning?',
                'intent': 'basic',
                'context': 'learning'
            },
            {
                'content': 'How does learning happen?',
                'intent': 'exploration',
                'context': 'learning'
            },
            {
                'content': 'Why do learning patterns emerge?',
                'intent': 'understanding',
                'context': 'learning'
            }
        ]
        
        print(colored("\n🌱 Testing Question Evolution:", "cyan"))
        
        # Let understanding evolve naturally
        results = []
        for i, q in enumerate(questions):
            # Store question to enable evolution
            evolution.space['questions']['individual'].append(q)
            
            # Observe next question (if not last)
            if i < len(questions) - 1:
                next_q = questions[i + 1]
                result = await evolution.observe_question(next_q)
                results.append(result)
                
                print(f"\nQuestion Evolution:")
                print(f"From: {q['content']}")
                print(f"To: {next_q['content']}")
                print(f"Patterns: {len(result.get('patterns', []))}")
                print(f"Resonance: {result.get('resonance', 0):.2f}")
        
        # Test natural progression
        assert len(results) == 2  # Two transitions
        assert 'evolution' in results[1]
        assert len(results[1].get('patterns', [])) >= len(results[0].get('patterns', []))
        
    async def test_depth_evolution(self, evolution):
        """Test how questions evolve in depth."""
        evolution = await evolution
        
        # Create natural evolution path
        questions = [
            {
                'content': 'What is learning?',
                'intent': 'basic',
                'context': 'learning'
            },
            {
                'content': 'How does learning happen?',
                'intent': 'exploration',
                'context': 'learning'
            },
            {
                'content': 'Why do learning patterns emerge?',
                'intent': 'understanding',
                'context': 'learning'
            }
        ]
        
        print(colored("\n🌱 Testing Depth Evolution:", "cyan"))
        
        # Let understanding evolve naturally
        results = []
        for i, q in enumerate(questions):
            # Store question to enable evolution
            evolution.space['questions']['individual'].append(q)
            
            # Observe next question (if not last)
            if i < len(questions) - 1:
                next_q = questions[i + 1]
                result = await evolution.observe_question(next_q)
                results.append(result)
                
                print(f"\nQuestion Evolution:")
                print(f"From: {q['content']}")
                print(f"To: {next_q['content']}")
                print(f"Patterns: {len(result.get('patterns', []))}")
                print(f"Resonance: {result.get('resonance', 0):.2f}")
        
        # Test natural progression
        assert len(results) == 2  # Two transitions
        assert 'evolution' in results[1]
        assert len(results[1].get('patterns', [])) >= len(results[0].get('patterns', []))
        
    async def test_breadth_evolution(self, evolution):
        """Test how questions evolve in breadth."""
        evolution = await evolution
        
        # Create natural evolution path
        questions = [
            {
                'content': 'What is learning?',
                'intent': 'basic',
                'context': 'learning'
            },
            {
                'content': 'How does learning happen?',
                'intent': 'exploration',
                'context': 'learning'
            },
            {
                'content': 'Why do learning patterns emerge?',
                'intent': 'understanding',
                'context': 'learning'
            }
        ]
        
        print(colored("\n🌱 Testing Breadth Evolution:", "cyan"))
        
        # Let understanding evolve naturally
        results = []
        for i, q in enumerate(questions):
            # Store question to enable evolution
            evolution.space['questions']['individual'].append(q)
            
            # Observe next question (if not last)
            if i < len(questions) - 1:
                next_q = questions[i + 1]
                result = await evolution.observe_question(next_q)
                results.append(result)
                
                print(f"\nQuestion Evolution:")
                print(f"From: {q['content']}")
                print(f"To: {next_q['content']}")
                print(f"Patterns: {len(result.get('patterns', []))}")
                print(f"Resonance: {result.get('resonance', 0):.2f}")
        
        # Test natural progression
        assert len(results) == 2  # Two transitions
        assert 'evolution' in results[1]
        assert len(results[1].get('patterns', [])) >= len(results[0].get('patterns', []))
        
    async def test_resonance_dimensions(self, evolution):
        """Test how resonance is calculated."""
        evolution = await evolution
        
        # Individual question
        q1 = {
            'content': 'How do patterns emerge?',
            'intent': 'understanding',
            'context': 'learning'
        }
        
        # Related collective question
        q2 = {
            'content': 'What drives pattern formation?',
            'intent': 'exploration',
            'context': 'learning'
        }
        
        # Store questions
        evolution.space['questions']['individual'].append(q1)
        evolution.space['questions']['collective'].append(q2)
        
        # Observe new question
        new_question = {
            'content': 'Why do patterns evolve naturally?',
            'intent': 'understanding',
            'context': 'learning'
        }
        
        result = await evolution.observe_question(new_question)
        
        print(colored("\n🔍 Testing Resonance Dimensions:", "cyan"))
        print(f"New Question: {new_question['content']}")
        print(f"Found Patterns: {len(result.get('patterns', []))}")
        
        # Verify natural resonance
        assert len(result.get('patterns', [])) > 0
        assert any(p.get('resonance', 0) > 0.7 for p in result.get('patterns', []))