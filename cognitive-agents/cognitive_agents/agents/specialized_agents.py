"""Specialized cognitive agents with distinct capabilities."""
from typing import Dict, List, Set
from datetime import datetime
from termcolor import colored
import json

from .cognitive_agent import CognitiveAgent

class PatternAnalyst(CognitiveAgent):
    """Tracks and evolves pattern understanding over time."""
    def __init__(self):
        super().__init__("Pattern Analyst", depth=1)
        self.pattern_history = []
        
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
        """Identify new patterns in current thought."""
        try:
            MIN_CONFIDENCE = 0.7
            
            # Check for minimal input first
            if len(thought.strip()) <= 4:  # "Fine", "Ok", etc
                minimal_pattern = {
                    "category": "surface",
                    "theme": "minimal response",
                    "confidence": 1.0
                }
                
                # Store in history
                self.pattern_history.append({
                    **minimal_pattern,
                    'timestamp': datetime.now().isoformat()
                })
                
                print(colored(f"\nFound minimal input pattern", "cyan"))
                return [minimal_pattern]
            
            system_prompt = """As a Pattern Analyst, identify patterns in this thought.
            Priority Order:
            1. Surface Patterns (obvious themes)
            2. Emotional Patterns (feelings, reactions)
            3. Behavioral Patterns (actions, responses)
            
            Important:
            - Respect input complexity (don't over-analyze simple inputs)
            - Only return high-confidence patterns (>= 0.7)
            - For very simple inputs (1-2 words), always use "surface" category
            
            Return as JSON array of objects with format:
            {
                "patterns": [
                    {
                        "category": "surface|emotional|behavioral",
                        "theme": "pattern theme",
                        "confidence": 0.0 to 1.0
                    }
                ]
            }"""
            
            response = await self.ai.chat.completions.create(
                model="gpt-3.5-turbo",
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
            
            # Parse response properly
            result = json.loads(response.choices[0].message.content)
            patterns = result.get('patterns', [])
            
            # Filter and log
            filtered_patterns = [p for p in patterns if p.get("confidence", 0) >= MIN_CONFIDENCE]
            print(colored(f"\nFound {len(filtered_patterns)} patterns", "cyan"))
            
            # Store patterns with thought context
            for pattern in filtered_patterns:
                self.pattern_history.append({
                    **pattern,
                    'thought': thought,  # Add the original thought
                    'timestamp': datetime.now().isoformat()
                })
            
            return filtered_patterns
            
        except Exception as e:
            print(colored(f"Error in pattern finding: {str(e)}", "red"))
            return []
    
    async def _analyze_pattern_correlations(self) -> List[Dict]:
        """Analyze patterns to find correlations between emotions and outcomes."""
        try:
            # Enhanced correlation prompt
            prompt = """As a Pattern Analyst, analyze this sequence of thoughts and patterns to identify recurring relationships.
            
            Focus especially on:
            1. How nervousness relates to outcomes
            2. Patterns of emotional states leading to achievements
            3. Recurring behavioral sequences
            
            Look for specific evidence of:
            - Emotional states preceding progress
            - Behavioral adaptations that work
            - Learning and growth patterns
            
            Return as JSON array of objects with format:
            {
                "correlations": [
                    {
                        "pattern": "clear description of recurring pattern",
                        "outcome": "what typically follows this pattern",
                        "evidence": ["specific example 1", "specific example 2"],
                        "confidence": 0.0 to 1.0,
                        "occurrences": number of times observed
                    }
                ]
            }"""
            
            # Build richer context
            history_entries = []
            for i, entry in enumerate(self.pattern_history):
                history_entries.append(
                    f"Entry {i+1}:\n"
                    f"Thought: {entry.get('thought', '')}\n"
                    f"Pattern: {entry.get('theme', '')}\n"
                    f"Category: {entry.get('category', '')}\n"
                    f"Confidence: {entry.get('confidence', 0)}\n"
                    f"---"
                )
            
            history_text = "\n".join(history_entries)
            
            response = await self.ai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": prompt
                }, {
                    "role": "user",
                    "content": f"Analyze these patterns:\n{history_text}"
                }],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            # Parse and filter correlations
            result = json.loads(response.choices[0].message.content)
            correlations = result.get('correlations', [])
            
            # Filter for high confidence and multiple occurrences
            filtered_correlations = [
                c for c in correlations 
                if c.get('confidence', 0) >= 0.7 and c.get('occurrences', 0) >= 2
            ]
            
            print(colored(f"\nFound {len(filtered_correlations)} strong correlations", "cyan"))
            return filtered_correlations
            
        except Exception as e:
            print(colored(f"Error analyzing correlations: {str(e)}", "red"))
            return []

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
                model="gpt-3.5-turbo",
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
                model="gpt-3.5-turbo",
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