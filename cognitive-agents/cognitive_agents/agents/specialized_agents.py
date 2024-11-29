"""Specialized cognitive agents with distinct capabilities."""
from typing import Dict, List, Set, Optional
from datetime import datetime
from termcolor import colored
import json

from .cognitive_agent import CognitiveAgent
from ..visualization.pattern_viz import PatternVisualizer
from ..pattern_store.db import PatternStore
from ..config import PATTERN_SETTINGS, CACHE_SETTINGS

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
    """Tracks and evolves pattern understanding over time."""
    def __init__(self):
        super().__init__("Pattern Analyst", depth=1)
        self.store = PatternStore()
        self.reset_state()
        
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
        """Identify new patterns in current thought with error recovery."""
        stored_patterns = []
        
        try:
            # Initialize sequence first
            if not self.current_sequence_id:
                sequence_type = self._detect_sequence_type(thought)
                self.current_sequence_id = self.store.create_sequence(sequence_type)
                print(colored(f"\nCreated new sequence: {sequence_type} (ID: {self.current_sequence_id})", "blue"))
            
            # Detect patterns
            patterns = await self._detect_patterns(thought)
            
            # Store each pattern
            for pattern in patterns:
                try:
                    pattern['timestamp'] = datetime.now().isoformat()
                    pattern['thought'] = thought
                    pattern_id = self.store.store_pattern(pattern, self.current_sequence_id)
                    pattern['id'] = pattern_id
                    
                    # Add to sequence
                    self.current_sequence.append({
                        'thought': thought,
                        'patterns': [pattern]
                    })
                    stored_patterns.append(pattern)
                    
                except Exception as e:
                    print(colored(f"Failed to store pattern: {str(e)}", "yellow"))
            
            return stored_patterns
            
        except PatternValidationError as e:
            print(colored(f"⚠️ Validation Error: {str(e)}", "yellow"))
            return self._handle_minimal_input(thought)  # Fallback to minimal
            
        except PatternDetectionError as e:
            print(colored(f"❌ Detection Error: {str(e)}", "red"))
            if stored_patterns:  # Return any patterns we found before error
                print(colored(f"↺ Recovered {len(stored_patterns)} patterns", "green"))
                return stored_patterns
            return self._handle_minimal_input(thought)  # Fallback if nothing found
            
        except PatternStorageError as e:
            print(colored(f"💾 Storage Error: {str(e)}", "red"))
            return stored_patterns  # Return patterns even if storage failed
            
        except Exception as e:
            print(colored(f"⚠️ Unexpected error in pattern finding: {str(e)}", "red"))
            if stored_patterns:
                return stored_patterns
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
            sequence_type = self._detect_sequence_type(thought)
            return self._apply_weights(cached_patterns, sequence_type)
        
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

class EmotionalExplorer(CognitiveAgent):
    """Builds emotional context and understanding over time."""
    def __init__(self):
        super().__init__("Emotional Explorer", depth=2)
        self.emotional_context = {
            'history': [],  # Emotional progression
            'themes': {},   # Recurring emotional themes
            'transitions': []  # Emotional shifts
        }
        
    async def _explore_emotional_depth(self, thought: str) -> Dict:
        """Explore emotional layers of the thought."""
        try:
            response = await self.ai.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",
                messages=[{
                    "role": "system",
                    "content": """As an Emotional Explorer, analyze the emotional layers in this thought.
                    Consider:
                    - Primary emotions
                    - Secondary emotions
                    - Emotional context
                    - Emotional patterns
                    - Emotional transitions
                    
                    Return a JSON object with format:
                    {
                        "primary_emotion": "emotion name",
                        "secondary_emotions": ["emotion1", "emotion2"],
                        "emotional_context": {
                            "situation": "context description",
                            "intensity": 0.0 to 1.0,
                            "triggers": ["trigger1", "trigger2"]
                        }
                    }"""
                }, {
                    "role": "user",
                    "content": thought
                }],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            emotional_layer = json.loads(response.choices[0].message.content)
            
            # Update emotional context
            self._update_emotional_context({
                'timestamp': datetime.now().isoformat(),
                'thought': thought,
                'analysis': emotional_layer
            })
            
            print(colored("\n💭 Emotional Layer:", "magenta"))
            print(f"  Primary: {emotional_layer.get('primary_emotion')}")
            print(f"  Context: {emotional_layer.get('emotional_context', {}).get('situation')}")
            
            return emotional_layer
            
        except Exception as e:
            print(colored(f"Error in emotional exploration: {str(e)}", "red"))
            return {}
    
    def _update_emotional_context(self, new_layer: Dict) -> None:
        """Update emotional context with new insights."""
        try:
            # Add to history
            self.emotional_context['history'].append(new_layer)
            
            # Update themes
            if 'analysis' in new_layer and 'primary_emotion' in new_layer['analysis']:
                primary = new_layer['analysis']['primary_emotion']
                if primary:
                    if primary not in self.emotional_context['themes']:
                        self.emotional_context['themes'][primary] = []
                    self.emotional_context['themes'][primary].append(new_layer['timestamp'])
            
            # Track transitions if there's history
            if len(self.emotional_context['history']) > 1:
                previous = self.emotional_context['history'][-2]
                current = new_layer
                
                if (previous.get('analysis', {}).get('primary_emotion') != 
                    current.get('analysis', {}).get('primary_emotion')):
                    self.emotional_context['transitions'].append({
                        'from': previous.get('analysis', {}).get('primary_emotion'),
                        'to': current.get('analysis', {}).get('primary_emotion'),
                        'timestamp': current['timestamp']
                    })
            
            print(colored("\n📊 Emotional Context Updated:", "blue"))
            print(f"  History entries: {len(self.emotional_context['history'])}")
            print(f"  Themes tracked: {len(self.emotional_context['themes'])}")
            print(f"  Transitions: {len(self.emotional_context['transitions'])}")
            
        except Exception as e:
            print(colored(f"Error updating emotional context: {str(e)}", "red"))

class IntegrationSynthesizer(CognitiveAgent):
    """Synthesizes insights across perspectives with memory."""
    def __init__(self):
        super().__init__("Integration Synthesizer", depth=3)
        self.insight_patterns = {
            'connections': [],    # Cross-perspective patterns
            'meta_themes': {},    # Higher-level understanding
            'evolution': []       # How understanding develops
        }
    
    async def integrate(self, pattern_insights: List[Dict], emotional_insights: Dict) -> Dict:
        """Integrate insights from different perspectives."""
        try:
            # Convert list to dict format expected by other methods
            patterns_dict = {"patterns": pattern_insights}
            
            # Find connections between patterns and emotions
            connections = self._find_cross_perspective_patterns(
                patterns_dict, 
                emotional_insights
            )
            
            # Build meta-understanding
            meta_understanding = await self._build_meta_cognition(
                connections,
                patterns_dict,
                emotional_insights
            )
            
            # Track evolution
            self.insight_patterns['evolution'].append({
                'timestamp': datetime.now().isoformat(),
                'patterns': len(pattern_insights),
                'connections': len(connections)
            })
            
            return {
                "meta_understanding": meta_understanding,
                "connections": connections,
                "patterns": pattern_insights,
                "emotions": emotional_insights
            }
            
        except Exception as e:
            print(colored(f"Integration error: {str(e)}", "red"))
            return {
                "meta_understanding": {},
                "connections": [],
                "patterns": [],
                "emotions": {}
            }
    
    def _find_cross_perspective_patterns(
        self, 
        pattern_insights: Dict, 
        emotional_insights: Dict
    ) -> List[Dict]:
        """Find meaningful connections between patterns and emotions."""
        connections = []
        
        # Get emotional context
        primary_emotion = emotional_insights.get('primary_emotion')
        emotional_context = emotional_insights.get('emotional_context', {})
        
        # Get patterns
        patterns = pattern_insights.get('patterns', [])
        
        # Look for connections
        for pattern in patterns:
            if emotional_context.get(pattern['theme']):
                connections.append({
                    'pattern': pattern['theme'],
                    'emotion': primary_emotion,
                    'context': emotional_context[pattern['theme']],
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