"""Enhanced cognitive agent with belief analysis capabilities."""

import asyncio
from typing import Dict, List, Optional
from termcolor import colored
import os
import json
from datetime import datetime
import hashlib

from .recursive_agent import RecursiveAgent
from ..config.spawn_config import SPAWN_CONFIG
from .base_agent import BaseAgent
from ..config import (
    CONSCIOUSNESS_THRESHOLDS,
    PATTERN_SETTINGS,
    PROCESSING_SETTINGS
)
from ..openai_client import AsyncOpenAI

class CognitiveAgent(BaseAgent):
    def __init__(self, role: str, depth: int = 0, **kwargs):
        """Initialize cognitive agent with optional kwargs for specialization.
        
        Args:
            role (str): Agent's role/purpose
            depth (int): Processing depth level
            **kwargs: Additional settings for specialized agents
                - max_depth: Maximum recursion depth
                - pattern_types: List of pattern types to detect
                - confidence_threshold: Minimum confidence threshold
        """
        self.role = role
        self.depth = depth
        self.pattern_memory = []
        
        # Optional specialized settings
        self.max_depth = kwargs.get('max_depth', CONSCIOUSNESS_THRESHOLDS['depth']['max'])
        self.pattern_types = kwargs.get('pattern_types', ['surface', 'emotional', 'behavioral', 'meta'])
        self.confidence_threshold = kwargs.get('confidence_threshold', PATTERN_SETTINGS['MIN_CONFIDENCE'])
        
        print(colored(f"Cognitive Agent '{role}' initialized at depth {depth}", "green"))

    async def process_thought(self, thought: str):
        """Process with consciousness-community awareness."""
        # Individual processing
        individual_understanding = await self.understand(thought)
        
        # Community integration
        collective_wisdom = await self.community_space.share(individual_understanding)
        
        # Natural evolution
        evolved_understanding = await self.integrate(
            individual_understanding,
            collective_wisdom
        )
        
        return evolved_understanding

    async def _analyze_thought(self, thought: str) -> Dict:
        """Analyze thought using AI to extract patterns and insights."""
        try:
            print(colored("\n Starting AI analysis...", "cyan"))
            client = AsyncOpenAI()
            
            # Calculate appropriate timeout
            timeout = self._calculate_timeout(thought)
            print(colored(f"⏱️  Using timeout: {timeout}s", "cyan"))
            
            # Use chat_with_retries with calculated timeout
            result = await client.chat_with_retries(
                messages=[{
                    "role": "system",
                    "content": """Analyze this thought and return a JSON response with patterns. Consider:
                    - Surface patterns (observable statements)
                    - Emotional patterns (feelings, reactions)
                    - Behavioral patterns (actions, responses)
                    - Meta patterns (higher-order insights)

                    Return response in this JSON format:
                    {
                        "insights": {
                            "integrated_understanding": {
                                "patterns": [
                                    "Surface patterns: ...",
                                    "Emotional patterns: ...",
                                    "Behavioral patterns: ...",
                                    "Meta patterns: ..."
                                ],
                                "analysis": "Overall analysis...",
                                "meta_cognition": "Higher-order insights..."
                            }
                        }
                    }"""
                }, {
                    "role": "user",
                    "content": thought
                }],
                timeout=timeout  # Pass timeout to chat_with_retries
            )
            
            print(colored("✅ AI analysis complete", "green"))
            return result
            
        except Exception as e:
            print(colored(f"❌ Error in AI analysis: {str(e)}", "red"))
            return self._create_empty_result()

    def _create_empty_result(self) -> Dict:
        """Create empty result structure."""
        return {
            "insights": {
                "integrated_understanding": {
                    "patterns": [],
                    "analysis": "",
                    "meta_cognition": ""
                }
            }
        }

    def _extract_patterns_from_insight(self, insight: Dict) -> List[Dict]:
        """Extract and standardize patterns from insight."""
        try:
            patterns = insight.get('insights', {}).get(
                'integrated_understanding', {}
            ).get('patterns', [])
            
            standardized_patterns = []
            for p in patterns:
                pattern_obj = {
                    'id': hashlib.sha256(str(p).encode()).hexdigest(),
                    'type': self._determine_pattern_type(p),
                    'content': str(p),
                    'confidence': self._calculate_pattern_confidence(p),
                    'timestamp': datetime.now().isoformat(),
                    'evidence': []
                }
                
                # Validate before adding
                if self._validate_pattern(pattern_obj):
                    standardized_patterns.append(pattern_obj)
                else:
                    print(colored(f"⚠️ Invalid pattern skipped: {p}", "yellow"))
            
            return standardized_patterns
            
        except Exception as e:
            print(colored(f"❌ Error extracting patterns: {str(e)}", "red"))
            return []

    def _calculate_integration_quality(self, patterns: List[Dict]) -> float:
        """Calculate integration quality score."""
        if not patterns:
            return 0.0
            
        # Consider pattern diversity
        pattern_types = {p['type'] for p in patterns}
        type_diversity = len(pattern_types) / 4  # Normalize by expected types
        
        # Consider confidence
        avg_confidence = sum(p['confidence'] for p in patterns) / len(patterns)
        
        return (type_diversity * 0.6 + avg_confidence * 0.4)

    def _determine_evolution_stage(self) -> str:
        """Determine current evolution stage."""
        if len(self.pattern_memory) >= CONSCIOUSNESS_THRESHOLDS['patterns']['complex']:
            return 'complex'
        elif len(self.pattern_memory) >= CONSCIOUSNESS_THRESHOLDS['patterns']['established']:
            return 'established'
        return 'emerging'

    def _calculate_confidence(self) -> float:
        """Calculate overall confidence."""
        return 0.7  # Base confidence, can be enhanced

    def _determine_pattern_type(self, pattern: str) -> str:
        """Determine pattern type from pattern string."""
        try:
            pattern_lower = pattern.lower()
            if pattern_lower.startswith('surface'):
                return 'surface'
            elif pattern_lower.startswith('emotional'):
                return 'emotional'
            elif pattern_lower.startswith('behavioral'):
                return 'behavioral'
            elif pattern_lower.startswith('meta'):
                return 'meta'
            return 'unknown'
        except Exception as e:
            print(colored(f"❌ Error determining pattern type: {str(e)}", "red"))
            return 'unknown'

    def _calculate_pattern_confidence(self, pattern: str) -> float:
        """Calculate confidence for a pattern."""
        try:
            # Basic confidence calculation
            if len(pattern) < 10:
                return 0.5
            elif len(pattern) < 30:
                return 0.7
            return 0.9
        except Exception as e:
            print(colored(f"❌ Error calculating confidence: {str(e)}", "red"))
            return 0.5

    def _calculate_timeout(self, thought: str) -> float:
        """Calculate appropriate timeout based on thought complexity."""
        # Base timeout
        timeout = 15.0
        
        # Adjust for thought length
        word_count = len(thought.split())
        if word_count > 50:
            timeout += 10.0
        elif word_count > 20:
            timeout += 5.0
        
        # Adjust for depth
        timeout += (self.depth * 2.0)
        
        # Cap maximum timeout
        return min(timeout, 30.0)

    def _create_result_structure(self, patterns: List[Dict], analysis: bool = True) -> Dict:
        """Create standardized result structure."""
        return {
            'patterns': patterns,
            'meta_synthesis': {
                'patterns_found': len(patterns),
                'integration_quality': self._calculate_integration_quality(patterns),
                'analysis_complete': analysis
            },
            'evolution': {
                'stage': self._determine_evolution_stage(),
                'confidence': self._calculate_confidence(),
                'timestamp': datetime.now().isoformat()
            }
        }

    def _validate_pattern(self, pattern: Dict) -> bool:
        """Validate pattern structure and content."""
        try:
            # Required fields
            required_fields = {'id', 'type', 'content', 'confidence', 'timestamp'}
            if not all(field in pattern for field in required_fields):
                return False
            
            # Type validation
            if pattern['type'] not in {'surface', 'emotional', 'behavioral', 'meta', 'unknown'}:
                return False
            
            # Content validation
            if not isinstance(pattern['content'], str) or len(pattern['content']) < 3:
                return False
            
            # Confidence validation
            if not (0.0 <= pattern['confidence'] <= 1.0):
                return False
            
            # Timestamp validation
            try:
                datetime.fromisoformat(pattern['timestamp'])
            except ValueError:
                return False
            
            return True
            
        except Exception as e:
            print(colored(f"❌ Pattern validation error: {str(e)}", "red"))
            return False

    def _update_pattern_memory(self, new_patterns: List[Dict]) -> None:
        """Update pattern memory avoiding duplicates."""
        try:
            # Get existing pattern IDs
            existing_ids = {p['id'] for p in self.pattern_memory}
            
            # Add only new patterns
            for pattern in new_patterns:
                if pattern['id'] not in existing_ids:
                    self.pattern_memory.append(pattern)
                    print(colored(f"📝 New pattern added: {pattern['type']}", "green"))
                
        except Exception as e:
            print(colored(f"❌ Error updating pattern memory: {str(e)}", "red"))

    def _is_pattern_relevant(self, pattern: Dict, thought: str) -> bool:
        """Determine if a pattern is relevant to current thought using enhanced criteria."""
        try:
            # Debug logging
            print(colored("\n🔍 Checking Pattern Relevance:", "cyan"))
            print(f"  Pattern: {pattern.get('content', '')}")
            print(f"  Thought: {thought}")
            
            # Basic relevance checks
            if not pattern or not thought:
                return False
            
            # Get pattern content as string
            pattern_content = pattern.get('content', '').lower()
            thought_lower = thought.lower()
            
            # 1. Word-based relevance
            pattern_words = set(pattern_content.split())
            thought_words = set(thought_lower.split())
            word_overlap = pattern_words.intersection(thought_words)
            word_score = len(word_overlap) / min(len(pattern_words), len(thought_words))
            print(f"  Word Score: {word_score:.2f}")
            
            # 2. Theme-based relevance
            themes = {
                'emotional': {'feel', 'emotion', 'mood', 'anxiety', 'nervous', 'worry', 'unknown', 'fear'},  # Added relevant words
                'behavioral': {'do', 'act', 'behave', 'respond', 'change'},
                'cognitive': {'think', 'believe', 'understand', 'know'},
                'meta': {'notice', 'observe', 'realize', 'pattern'}
            }
            
            pattern_type = pattern.get('type', 'unknown')
            theme_words = themes.get(pattern_type, set())
            theme_overlap = thought_words.intersection(theme_words)
            theme_score = len(theme_overlap) * 0.3  # Increased theme weight
            print(f"  Theme Score: {theme_score:.2f}")
            
            # 3. Calculate final relevance score
            relevance_score = word_score + theme_score
            
            # Apply type-based boosts
            if pattern_type in {'emotional', 'meta'}:
                relevance_score *= 1.2
            
            # Consider pattern confidence
            confidence = pattern.get('confidence', 0.0)
            final_score = relevance_score * confidence
            print(f"  Final Score: {final_score:.2f}")
            print(f"  Required: {self.confidence_threshold * 0.7:.2f}")
            
            is_relevant = final_score >= (self.confidence_threshold * 0.7)
            print(colored(f"  Relevant: {is_relevant}", "green" if is_relevant else "red"))
            
            return is_relevant
            
        except Exception as e:
            print(colored(f"❌ Error checking pattern relevance: {str(e)}", "red"))
            return False

class AdaptiveTimeout:
    def __init__(self):
        self.timeout_history = []
        self.MAX_HISTORY = 50  # Reduced from 100
        
    def calculate_timeout(self, thought: str, has_previous_patterns: bool) -> int:
        """Calculate adaptive timeout based on complexity."""
        try:
            # Simple base timeout
            base_timeout = 10  # Base: 10 seconds
            
            # Basic complexity factors
            if len(thought.split()) > 15:  # Length
                base_timeout += 2
                
            if has_previous_patterns:  # Context
                base_timeout += 3
                
            # Update history
            self.timeout_history.append(base_timeout)
            if len(self.timeout_history) > self.MAX_HISTORY:
                self.timeout_history.pop(0)
                
            return base_timeout
            
        except Exception as e:
            print(colored(f"Timeout calculation error: {str(e)}", "red"))
            return 10  # Default safe timeout
  