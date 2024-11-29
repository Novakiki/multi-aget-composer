"""Specialized cognitive agents with distinct capabilities."""
from typing import Dict, List, Set, Optional, Union
from datetime import datetime
from termcolor import colored
import json
import asyncio
import hashlib
import os

from .cognitive_agent import CognitiveAgent
from ..visualization.pattern_viz import PatternVisualizer
from ..pattern_store.db import PatternStore
from ..config import PATTERN_SETTINGS, CACHE_SETTINGS, PROCESSING_SETTINGS
from ..openai_client import AsyncOpenAI
from sentence_transformers import SentenceTransformer
import numpy as np

class PatternError(Exception):
    """Base class for pattern-related errors."""
    pass

class PatternDetectionError(PatternError):
    """Error during pattern detection."""
    pass

class PatternValidationError(PatternError):
    """Error during pattern validation."""
    pass

class PatternStorageError(PatternError):
    """Error during pattern storage."""
    pass

class PatternAnalyst(CognitiveAgent):
    """Specialized agent for deep pattern analysis and evolution tracking."""
    
    def __init__(self):
        super().__init__("Pattern Analyst", depth=1)
        self.client = AsyncOpenAI()
        self.pattern_history = []
        self.pattern_evolution = {
            'themes': {},      # Track theme development
            'transitions': [], # Pattern transitions
            'meta': set()     # Meta-patterns
        }
        
    async def analyze_pattern_sequence(self, thoughts: List[str]) -> Dict:
        """Analyze sequence of thoughts for pattern evolution."""
        try:
            sequence_patterns = []
            for thought in thoughts:
                # Get patterns for this thought
                patterns = await self._find_new_patterns(thought)
                sequence_patterns.append({
                    'thought': thought,
                    'patterns': patterns,
                    'timestamp': datetime.now().isoformat()
                })
                
                # Track theme evolution
                self._update_theme_evolution(patterns)
                
                # Track transitions
                if len(sequence_patterns) > 1:
                    self._track_pattern_transition(
                        sequence_patterns[-2]['patterns'],
                        patterns
                    )
            
            # Generate meta-insights
            meta_insights = self._synthesize_meta_patterns(sequence_patterns)
            
            return {
                'sequence_patterns': sequence_patterns,
                'theme_evolution': self.pattern_evolution['themes'],
                'transitions': self.pattern_evolution['transitions'],
                'meta_insights': list(meta_insights)
            }
            
        except Exception as e:
            print(colored(f"❌ Error in sequence analysis: {str(e)}", "red"))
            return {}
            
    def _update_theme_evolution(self, patterns: List[Dict]) -> None:
        """Track how themes evolve over time."""
        for pattern in patterns:
            theme = pattern.get('theme')
            if not theme:
                continue
                
            if theme not in self.pattern_evolution['themes']:
                self.pattern_evolution['themes'][theme] = {
                    'first_seen': datetime.now().isoformat(),
                    'occurrences': 0,
                    'confidence_history': [],
                    'related_patterns': set()
                }
                
            theme_data = self.pattern_evolution['themes'][theme]
            theme_data['occurrences'] += 1
            theme_data['confidence_history'].append(pattern.get('confidence', 0))
            theme_data['related_patterns'].add(pattern.get('content'))
            
    def _track_pattern_transition(
        self,
        previous_patterns: List[Dict],
        current_patterns: List[Dict]
    ) -> None:
        """Track how patterns transition and evolve."""
        for prev in previous_patterns:
            for curr in current_patterns:
                if self._patterns_are_related(prev, curr):
                    transition = {
                        'from_pattern': prev['content'],
                        'to_pattern': curr['content'],
                        'timestamp': datetime.now().isoformat(),
                        'confidence': min(
                            prev.get('confidence', 0),
                            curr.get('confidence', 0)
                        )
                    }
                    self.pattern_evolution['transitions'].append(transition)
                    
    def _patterns_are_related(self, pattern1: Dict, pattern2: Dict) -> bool:
        """Check if two patterns are related."""
        # Get words from each pattern
        words1 = set(pattern1.get('content', '').lower().split())
        words2 = set(pattern2.get('content', '').lower().split())
        
        # Calculate overlap
        overlap = len(words1.intersection(words2))
        overlap_ratio = overlap / min(len(words1), len(words2))
        
        # Check theme relationship
        same_type = pattern1.get('type') == pattern2.get('type')
        
        return overlap_ratio >= 0.3 or same_type
    
    def reset_state(self):
        """Reset agent state between sequences while preserving cache."""
        self.pattern_history = []
        self.current_sequence = []
        self.current_sequence_id = None
        self.visualizer = PatternVisualizer()
        self.store.cleanup_sequences()
        
    def _analyze_pattern_history(self) -> List[Dict]:
        """Find patterns that evolve over time."""
        patterns_by_theme = {}
        
        for entry in self.pattern_history:
            theme = entry['theme']
            if theme not in patterns_by_theme:
                patterns_by_theme[theme] = []
            patterns_by_theme[theme].append(entry)
            
        print(colored("\n📈 Pattern Evolution:", "cyan"))
        for theme, entries in patterns_by_theme.items():
            print(f"  Theme: {theme}")
            print(f"  Occurrences: {len(entries)}")
            print(f"  First seen: {entries[0]['timestamp']}")
            
        return patterns_by_theme
    
    async def _find_new_patterns(self, thought: str) -> List[Dict]:
        """Find patterns in thought."""
        try:
            result = await self.client.chat_with_retries(
                messages=[{
                    "role": "system",
                    "content": """Analyze this thought for patterns. Return JSON with format:
                    {
                        "patterns": [
                            {
                                "category": "emotional/behavioral/cognitive/meta",
                                "theme": "pattern description",
                                "confidence": 0.8,
                                "evidence": ["supporting detail 1", "supporting detail 2"]
                            }
                        ]
                    }"""
                }, {
                    "role": "user",
                    "content": thought
                }]
            )
            
            patterns = result.get('patterns', [])
            self.pattern_history.extend(patterns)
            return patterns
            
        except Exception as e:
            print(colored(f"⚠️ Pattern detection failed: {str(e)}", "yellow"))
            return []
    
    async def _analyze_pattern_correlations(self) -> Dict:
        """Analyze patterns with sequence context."""
        try:
            # Track pattern types for summary
            pattern_summary = {
                'emotional': 0,
                'behavioral': 0,
                'surface': 0,
                'meta': 0
            }
            
            # Count patterns once at the start
            for entry in self.current_sequence:
                for pattern in entry['patterns']:
                    category = pattern.get('category', 'unknown')
                    if category in pattern_summary:
                        pattern_summary[category] += 1
            
            # Build transitions from sequence
            transitions = []
            for i in range(len(self.current_sequence)-1):
                current = self.current_sequence[i]
                next_step = self.current_sequence[i+1]
                
                # Get patterns from each step
                try:
                    for current_pattern in current['patterns']:
                        for next_pattern in next_step['patterns']:
                            transition = {
                                'pattern': current_pattern['theme'],
                                'outcome': next_pattern['theme'],
                                'evidence': [
                                    f"From: {current['thought']}",
                                    f"To: {next_step['thought']}"
                                ],
                                'confidence': min(
                                    current_pattern['confidence'], 
                                    next_pattern['confidence']
                                )
                            }
                            transitions.append(transition)
                except (KeyError, IndexError) as e:
                    print(colored(f"⚠️ Skipping invalid pattern: {str(e)}", "yellow"))
                    continue
            
            # Filter for high confidence
            filtered_correlations = [
                t for t in transitions 
                if t['confidence'] >= PATTERN_SETTINGS['MIN_CONFIDENCE']
            ]
            
            return {
                'correlations': filtered_correlations,
                'summary': pattern_summary
            }
            
        except Exception as e:
            print(colored(f"Error analyzing correlations: {str(e)}", "red"))
            return {
                'correlations': [],
                'summary': {}
            }
    
    def _detect_sequence_type(self, thought: str) -> str:
        """Detect sequence type from thought content."""
        thought_lower = thought.lower()
        
        for seq_type, keywords in PATTERN_SETTINGS['SEQUENCE_TYPES'].items():
            if any(keyword in thought_lower for keyword in keywords):
                return seq_type
            
        return "emotional"  # default
    
    def _handle_minimal_input(self, thought: str) -> List[Dict]:
        """Handle minimal input with basic pattern detection."""
        minimal_pattern = {
            "category": "surface",
            "theme": "minimal response",
            "confidence": 1.0,
            "timestamp": datetime.now().isoformat(),
            "thought": thought
        }
        
        # Store in history
        self.pattern_history.append(minimal_pattern)
        print(colored(f"\nHandled minimal input", "cyan"))
        return [minimal_pattern]
    
    async def _detect_patterns(self, thought: str) -> List[Dict]:
        """Core pattern detection logic with caching."""
        MIN_CONFIDENCE = PATTERN_SETTINGS['MIN_CONFIDENCE']
        
        # Try cache first
        cached_patterns = self.store.get_cached_patterns(thought)
        if cached_patterns:
            if CACHE_SETTINGS['METRICS_ENABLED']:
                metrics = self.store.get_cache_metrics()
                print(colored("\n📊 Cache Metrics:", "blue"))
                print(f"  Total Entries: {metrics['total_entries']}")
                print(f"  Total Hits: {metrics['total_hits']}")
                print(f"  Avg Hits/Entry: {metrics['avg_hits']:.1f}")
                print(f"  Avg Age: {metrics['avg_age_days']:.1f} days")
            
            print(colored("📦 Using cached patterns", "green"))
            
            # Normalize cached patterns
            normalized_patterns = []
            for pattern in cached_patterns:
                if isinstance(pattern, dict):
                    if 'patterns' in pattern:
                        normalized_patterns.extend(pattern['patterns'])
                    elif all(k in pattern for k in ['category', 'theme', 'confidence']):
                        normalized_patterns.append(pattern)
            
            sequence_type = self._detect_sequence_type(thought)
            return self._apply_weights(normalized_patterns, sequence_type)
        
        try:
            # Normal AI-based detection
            patterns = await self._detect_patterns_from_ai(thought)
            
            # Cache the results
            self.store.cache_pattern(thought, patterns)
            
            # Apply weights and return
            sequence_type = self._detect_sequence_type(thought)
            return self._apply_weights(patterns, sequence_type)
            
        except Exception as e:
            print(colored(f"⚠️ Pattern detection failed: {str(e)}", "red"))
            return []
    
    def _apply_weights(self, patterns: List[Dict], sequence_type: str) -> List[Dict]:
        """Apply sequence-specific weights to patterns."""
        weights = PATTERN_SETTINGS['PATTERN_WEIGHTS'].get(sequence_type, {
            'emotional': 1.0,
            'behavioral': 1.0,
            'surface': 1.0,
            'meta': 1.0
        })
        
        weighted_patterns = []
        for pattern in patterns:
            category = pattern.get('category', 'unknown')
            weight = weights.get(category, 1.0)
            pattern['confidence'] = min(1.0, pattern['confidence'] * weight)
            weighted_patterns.append(pattern)
        
        return [p for p in weighted_patterns if p['confidence'] >= PATTERN_SETTINGS['MIN_CONFIDENCE']]
    
    async def _store_patterns(self, patterns: List[Dict], thought: str) -> List[Dict]:
        """Store patterns with proper error handling."""
        stored_patterns = []
        
        # Initialize sequence if needed
        if not self.current_sequence_id:
            sequence_type = self._detect_sequence_type(thought)
            self.current_sequence_id = self.store.create_sequence(sequence_type)
        
        # Store each pattern
        for pattern in patterns:
            try:
                # Add metadata
                pattern['timestamp'] = datetime.now().isoformat()
                pattern['thought'] = thought
                
                # Store in database
                pattern_id = self.store.store_pattern(
                    pattern,
                    self.current_sequence_id
                )
                pattern['id'] = pattern_id
                
                # Add to sequence
                self.current_sequence.append({
                    'thought': thought,
                    'patterns': [pattern]
                })
                
                stored_patterns.append(pattern)
                
            except Exception as e:
                print(colored(f"Failed to store pattern: {str(e)}", "yellow"))
                continue
        
        return stored_patterns
    
    async def _detect_patterns_from_ai(self, thought: str) -> List[Dict]:
        """Core AI-based pattern detection."""
        system_prompt = """As a Pattern Analyst, identify organic patterns in thoughts.

Core Principles:
1. Natural Emergence
   - Let patterns surface naturally from the content
   - Identify emotional states and transitions
   - Recognize behavioral patterns
   - Track progression over time

2. Pattern Types:
   • Emotional: Feelings, reactions, states (e.g., uncertainty → confidence)
   • Behavioral: Actions, responses (e.g., hesitation → action)
   • Surface: Observable statements, facts
   • Meta: Pattern evolution and connections

3. Pattern Validation
   - Each pattern must have clear evidence
   - Assign confidence based on clarity (0.7-1.0)
   - Look for recurring themes and transitions

4. Sequence Awareness
   - Track emotional progression
   - Note behavioral changes
   - Identify transition points

Return as JSON:
{
    "patterns": [
        {
            "category": "emotional|behavioral|surface|meta",
            "theme": "specific pattern description",
            "confidence": 0.0 to 1.0,
            "evidence": ["supporting detail"],
            "sequence_context": "how this fits in progression"
        }
    ]
}"""
        
        response = await self.ai.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{
                "role": "system",
                "content": system_prompt
            }, {
                "role": "user",
                "content": thought
            }],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get('patterns', [])
    
    async def _process_entries(self, entries: List[str]) -> List[Dict]:
        """Process entries in parallel while maintaining deep analysis."""
        print(colored("\n🔄 Processing Entries in Parallel", "cyan"))
        print(f"  Total entries: {len(entries)}")
        
        try:
            # Input validation
            if not entries:
                print(colored("⚠️ No entries to process", "yellow"))
                return []
            
            # Create tasks for parallel processing
            tasks = []
            for entry in entries:
                try:
                    task = self._find_new_patterns(entry)
                    tasks.append(task)
                except Exception as e:
                    print(colored(f"⚠️ Failed to create task for entry: {str(e)}", "yellow"))
            
            if not tasks:
                print(colored("❌ No valid tasks created", "red"))
                return []
            
            # Execute all tasks concurrently with timeout
            try:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Filter out exceptions and empty results
                valid_results = []
                for i, result in enumerate(results):
                    if isinstance(result, Exception):
                        print(colored(f"❌ Entry {i} failed: {str(result)}", "red"))
                    elif result:
                        valid_results.append(result)
                
                # Flatten results while preserving all patterns
                all_patterns = [
                    pattern 
                    for result in valid_results 
                    for pattern in result
                ]
                
                print(f"  Total patterns found: {len(all_patterns)}")
                if all_patterns:
                    print(f"  Average patterns per entry: {len(all_patterns)/len(entries):.1f}")
                
                return all_patterns
                
            except asyncio.TimeoutError:
                print(colored("❌ Parallel processing timed out", "red"))
                return []
                
        except Exception as e:
            print(colored(f"❌ Parallel processing error: {str(e)}", "red"))
            print(colored(f"  Error type: {type(e).__name__}", "red"))
            return []

class EmotionalExplorer(CognitiveAgent):
    """Specialized agent for emotional pattern analysis."""
    
    def __init__(self):
        super().__init__("Emotional Explorer", depth=2)
        self.emotional_context = {
            'history': [],
            'themes': set(),
            'transitions': []
        }
        self.client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    async def _explore_emotional_depth(self, thought: str) -> Dict:
        """Explore emotional depth of thought."""
        try:
            result = await self._analyze_emotion(thought)
            
            # Add to emotional context with thought included
            self.emotional_context['history'].append({
                'thought': thought,  # Add the original thought
                'timestamp': datetime.now().isoformat(),
                'analysis': result
            })
            
            print(colored("\n📊 Emotional Context Updated:", "cyan"))
            print(f"  History entries: {len(self.emotional_context['history'])}")
            print(f"  Themes tracked: {len(self.emotional_context['themes'])}")
            print(f"  Transitions: {len(self.emotional_context['transitions'])}")
            
            return result
            
        except Exception as e:
            print(colored(f"❌ Error in emotional exploration: {str(e)}", "red"))
            return {}

    def _update_emotional_context(self, result: Dict, thought: str) -> None:
        """Update emotional context with new insights."""
        try:
            # Add single entry with both analysis and thought
            entry = {
                'timestamp': datetime.now().isoformat(),
                'thought': thought,
                'analysis': result
            }
            
            # Replace any existing entries for this thought
            existing_entries = [
                i for i, e in enumerate(self.emotional_context['history']) 
                if e.get('thought') == thought
            ]
            if existing_entries:
                self.emotional_context['history'][existing_entries[0]] = entry
            else:
                self.emotional_context['history'].append(entry)
            
            # Track themes and transitions
            if 'themes' in result.get('emotional_context', {}):
                self.emotional_context['themes'].update(
                    result['emotional_context']['themes']
                )
            
            # Track transitions
            if len(self.emotional_context['history']) > 1:
                previous = self.emotional_context['history'][-2]
                if (previous['analysis']['primary_emotion'] != 
                    result['primary_emotion']):
                    self.emotional_context['transitions'].append({
                        'from': previous['analysis']['primary_emotion'],
                        'to': result['primary_emotion'],
                        'timestamp': entry['timestamp']
                    })
            
        except Exception as e:
            print(colored(f"Error updating emotional context: {str(e)}", "red"))

    async def _analyze_emotion(self, thought: str) -> Dict:
        """Analyze emotional content of thought."""
        try:
            result = await self.client.chat_with_retries(
                messages=[{
                    "role": "system",
                    "content": """Analyze the emotional content of this thought.
                    Return JSON with format:
                    {
                        "primary_emotion": "main emotion",
                        "secondary_emotions": ["other", "emotions"],
                        "emotional_context": {
                            "situation": "context description",
                            "intensity": 0.7,
                            "themes": ["theme1", "theme2"]
                        }
                    }"""
                }, {
                    "role": "user",
                    "content": thought
                }]
            )
            
            # Update emotional context
            self._update_emotional_context(result, thought)
            
            return result
            
        except Exception as e:
            print(colored(f"❌ Error analyzing emotion: {str(e)}", "red"))
            return {
                "primary_emotion": "unknown",
                "secondary_emotions": [],
                "emotional_context": {
                    "situation": "",
                    "intensity": 0.0,
                    "themes": []
                }
            }

class IntegrationSynthesizer(CognitiveAgent):
    """Synthesizes insights across perspectives with memory."""
    def __init__(self):
        super().__init__("Integration Synthesizer", depth=3)
        self.client = AsyncOpenAI()
        self.insight_patterns = {
            'evolution': [],
            'connections': [],
            'meta': []
        }
    
    async def integrate(self, patterns: List[Dict], emotions: Dict) -> Dict:
        """Integrate patterns and emotions into higher understanding."""
        try:
            result = await self.client.chat_with_retries(
                messages=[{
                    "role": "system",
                    "content": """Integrate patterns and emotions into meta-understanding.
                    Return JSON with format:
                    {
                        "meta_understanding": {
                            "themes": ["theme1", "theme2"],
                            "insights": ["insight1", "insight2"],
                            "evolution": {
                                "stage": "stage_name",
                                "direction": "direction_name"
                            }
                        }
                    }"""
                }, {
                    "role": "user",
                    "content": json.dumps({
                        "patterns": patterns,
                        "emotions": emotions
                    })
                }]
            )
            
            return result
            
        except Exception as e:
            print(colored(f"❌ Integration error: {str(e)}", "red"))
            return {}
    
    def _find_cross_perspective_patterns(
        self, 
        pattern_insights: Dict, 
        emotional_insights: Dict
    ) -> List[Dict]:
        """Find meaningful connections between patterns and emotions."""
        connections = []
        
        # Get emotional context safely
        emotional_context = emotional_insights.get('emotional_context', {})
        if not isinstance(emotional_context, dict):
            emotional_context = {}
        
        # Get patterns safely
        patterns = pattern_insights.get('patterns', [])
        if not isinstance(patterns, list):
            patterns = []
        
        # Look for connections
        for pattern in patterns:
            theme = pattern.get('theme', '')
            if theme and emotional_context.get('situation'):
                connections.append({
                    'pattern': theme,
                    'emotion': emotional_insights.get('primary_emotion'),
                    'context': emotional_context.get('situation'),
                    'timestamp': datetime.now().isoformat()
                })
        
        print(colored("\n🔗 Cross-Perspective Connections:", "green"))
        print(f"  Found {len(connections)} connections")
        for conn in connections:
            print(f"  • {conn['pattern']} ↔ {conn['emotion']}")
            
        return connections
    
    async def _build_meta_cognition(
        self,
        connections: List[Dict],
        pattern_insights: Dict,
        emotional_insights: Dict
    ) -> Dict:
        """Build higher-level understanding from connections."""
        try:
            # Create meta-cognitive prompt
            prompt = f"""As an Integration Synthesizer, analyze these perspectives:
            
            Pattern Insights: {pattern_insights}
            Emotional Context: {emotional_insights}
            Found Connections: {connections}
            
            Build a meta-cognitive understanding that:
            1. Identifies higher-level themes
            2. Traces how understanding evolves
            3. Finds meaningful connections
            
            Return a JSON object with this meta-understanding."""
            
            response = await self.ai.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",
                messages=[{
                    "role": "system",
                    "content": prompt
                }],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            meta_understanding = json.loads(response.choices[0].message.content)
            
            print(colored("\n🧠 Meta Understanding:", "magenta"))
            print(f"  Themes: {len(meta_understanding.get('themes', []))}")
            print(f"  Evolution: {meta_understanding.get('evolution_stage')}")
            
            return meta_understanding
            
        except Exception as e:
            print(colored(f"Meta-cognition error: {str(e)}", "red"))
            return {}
    
    def _track_insight_evolution(self, meta_understanding: Dict) -> None:
        """Track how insights evolve over time."""
        try:
            self.insight_patterns['evolution'].append({
                'timestamp': datetime.now().isoformat(),
                'understanding': meta_understanding,
                'depth': self.depth
            })
        except Exception as e:
            print(colored(f"Error tracking evolution: {str(e)}", "red"))

class CognitiveOrchestrator:
    """Manages agent coordination and parallel processing."""
    
    def __init__(self):
        self.pattern_analyst = PatternAnalyst()
        self.emotional_explorer = EmotionalExplorer()
        self.integration_synthesizer = IntegrationSynthesizer()
    
    async def process_thoughts(self, thoughts: Union[str, List[str]]) -> Dict:
        """Process single or multiple thoughts."""
        if isinstance(thoughts, str):
            return await self._process_single(thoughts)
        
        if len(thoughts) >= 3:
            return await self._process_batch(thoughts)
        
        return await self._process_sequential(thoughts)
    
    async def _process_single(self, thought: str) -> Dict:
        """Process single thought with parallel agents."""
        try:
            # Create tasks
            pattern_task = self.pattern_analyst._find_new_patterns(thought)
            emotion_task = self.emotional_explorer._explore_emotional_depth(thought)
            
            # Use asyncio.wait_for instead of timeout in gather
            patterns = await asyncio.wait_for(
                pattern_task,
                timeout=PROCESSING_SETTINGS['TIMEOUT']
            )
            emotions = await asyncio.wait_for(
                emotion_task,
                timeout=PROCESSING_SETTINGS['TIMEOUT']
            )
            
            # Integration needs both results
            synthesis = await self.integration_synthesizer.integrate(
                patterns, emotions
            )
            
            return {
                "patterns": patterns,
                "emotions": emotions,
                "synthesis": synthesis
            }
            
        except asyncio.TimeoutError:
            print(colored("❌ Processing timeout", "red"))
            return {}
        except Exception as e:
            print(colored(f"❌ Processing error: {str(e)}", "red"))
            return {}
    
    async def _process_batch(self, thoughts: List[str]) -> Dict:
        """Process multiple thoughts in parallel."""
        results = []
        for thought in thoughts:
            result = await self._process_single(thought)
            results.append(result)
        
        return {
            "results": results,
            "batch_size": len(thoughts),
            "processing_mode": "batch"
        }
    
    async def _process_sequential(self, thoughts: List[str]) -> Dict:
        """Process thoughts sequentially for small batches."""
        results = []
        for thought in thoughts:
            result = await self._process_single(thought)
            results.append(result)
        return {"results": results}

class HybridPatternAnalyst(PatternAnalyst):
    """Enhanced pattern analyst with hybrid symbolic-vector analysis."""
    
    def __init__(self):
        super().__init__()
        # Initialize vector model
        self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
        # Add vector storage
        self.vector_memory = {
            'embeddings': [],  # Store vectors
            'thoughts': [],    # Store original thoughts
            'timestamps': []   # Store when added
        }
        
    async def analyze_thought(self, thought: str) -> Dict:
        """Analyze thought using both symbolic and vector approaches."""
        try:
            print(colored("\n🔍 Starting hybrid analysis...", "cyan"))
            
            # 1. Traditional pattern analysis
            symbolic_patterns = await self._find_new_patterns(thought)
            print(colored(f"Found {len(symbolic_patterns)} symbolic patterns", "green"))
            
            # 2. Vector analysis
            vector = self.semantic_model.encode(thought)
            self._store_vector(vector, thought)
            similar_thoughts = self._find_similar_thoughts(vector)
            print(colored(f"Found {len(similar_thoughts)} similar thoughts", "green"))
            
            # Create proper result structure
            result = {
                'patterns': symbolic_patterns,
                'similar_thoughts': similar_thoughts,  # Make sure this exists
                'synthesis': {
                    'interpretable_insights': [],
                    'semantic_connections': [],
                    'explanation': ''
                }
            }
            
            # Add insights from patterns
            for pattern in symbolic_patterns:
                result['synthesis']['interpretable_insights'].append({
                    'type': pattern['type'],
                    'content': pattern['content'],
                    'confidence': pattern['confidence'],
                    'explanation': f"Pattern found: {pattern['type']}"
                })
            
            # Add semantic connections
            for similar in similar_thoughts:
                result['synthesis']['semantic_connections'].append({
                    'thought': similar['thought'],
                    'similarity': similar['score'],
                    'explanation': f"Semantic similarity: {similar['score']:.2f}"
                })
            
            return result
            
        except Exception as e:
            print(colored(f"❌ Error in hybrid analysis: {str(e)}", "red"))
            # Return valid structure even on error
            return {
                'patterns': [],
                'similar_thoughts': [],
                'synthesis': {
                    'interpretable_insights': [],
                    'semantic_connections': [],
                    'explanation': f"Analysis error: {str(e)}"
                }
            }
    
    def _store_vector(self, vector: np.ndarray, thought: str) -> None:
        """Store vector with metadata."""
        self.vector_memory['embeddings'].append(vector)
        self.vector_memory['thoughts'].append(thought)
        self.vector_memory['timestamps'].append(datetime.now().isoformat())
        
    def _find_similar_thoughts(self, query_vector: np.ndarray) -> List[Dict]:
        """Find similar thoughts using vector similarity."""
        if not self.vector_memory['embeddings']:
            return []
            
        # Calculate similarities
        similarities = [
            np.dot(query_vector, stored_vec) 
            for stored_vec in self.vector_memory['embeddings']
        ]
        
        # Get top matches
        matches = []
        for i, score in enumerate(similarities):
            if score > 0.7:  # Similarity threshold
                matches.append({
                    'thought': self.vector_memory['thoughts'][i],
                    'score': float(score),
                    'timestamp': self.vector_memory['timestamps'][i]
                })
                
        return sorted(matches, key=lambda x: x['score'], reverse=True)
        
    def _combine_analyses(
        self,
        symbolic_patterns: List[Dict],
        similar_thoughts: List[Dict],
        current_thought: str
    ) -> Dict:
        """Combine symbolic and vector analyses with explanations."""
        combined = {
            'patterns': symbolic_patterns,
            'similar_thoughts': similar_thoughts,
            'synthesis': {
                'interpretable_insights': [],
                'semantic_connections': [],
                'explanation': ''
            }
        }
        
        # Add interpretable insights
        for pattern in symbolic_patterns:
            insight = {
                'type': pattern['type'],
                'content': pattern['content'],
                'confidence': pattern['confidence'],
                'explanation': f"Recognized through {pattern['type']} pattern matching"
            }
            combined['synthesis']['interpretable_insights'].append(insight)
        
        # Add semantic connections
        for match in similar_thoughts:
            connection = {
                'thought': match['thought'],
                'similarity': match['score'],
                'explanation': f"Semantically similar with {match['score']:.2f} confidence"
            }
            combined['synthesis']['semantic_connections'].append(connection)
        
        # Generate overall explanation
        combined['synthesis']['explanation'] = self._generate_synthesis_explanation(
            symbolic_patterns,
            similar_thoughts
        )
        
        return combined
    
    def _generate_synthesis_explanation(
        self,
        symbolic_patterns: List[Dict],
        similar_thoughts: List[Dict]
    ) -> str:
        """Generate human-readable synthesis explanation."""
        try:
            explanations = []
            
            # Explain symbolic patterns
            if symbolic_patterns:
                pattern_types = set(p['type'] for p in symbolic_patterns)
                explanations.append(
                    f"Found {len(symbolic_patterns)} patterns "
                    f"of types: {', '.join(pattern_types)}"
                )
            
            # Explain semantic connections
            if similar_thoughts:
                top_match = similar_thoughts[0]
                explanations.append(
                    f"Most similar previous thought "
                    f"(similarity: {top_match['score']:.2f}): "
                    f"{top_match['thought']}"
                )
            
            # Combine explanations
            if explanations:
                return "\n".join(explanations)
            return "No significant patterns or similarities found."
            
        except Exception as e:
            print(colored(f"❌ Error generating explanation: {str(e)}", "red"))
            return "Error generating explanation."