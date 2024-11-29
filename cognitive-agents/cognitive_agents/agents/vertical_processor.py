from typing import Dict, List, Optional
from termcolor import colored
import asyncio
import os

from .cognitive_agent import CognitiveAgent

class VerticalProcessor:
    """Implements vertical (depth) processing capabilities."""
    
    def __init__(self):
        self.depth_levels = {
            'surface': {
                'role': 'Initial pattern recognition',
                'features': ['quick pattern detection', 'basic categorization']
            },
            'intermediate': {
                'role': 'Connection analysis',
                'features': ['pattern_connections', 'context_building']
            },
            'deep': {
                'role': 'Meta-pattern synthesis',
                'features': ['meta_patterns', 'systemic_insights']
            }
        }
        print(colored("Vertical Processor initialized", "green"))

    async def process_at_depth(
        self, 
        thought: str, 
        depth_level: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """Process thought at specified depth level."""
        try:
            print(colored(f"\n🔍 Processing at {depth_level} level", "cyan"))
            
            # Create depth-specific agent
            agent = self._create_depth_agent(depth_level)
            
            # Process with depth-specific context
            enhanced_thought = self._enhance_for_depth(thought, depth_level, context)
            result = await agent.process_thought(enhanced_thought)
            
            # Extract depth-specific patterns
            patterns = self._extract_depth_patterns(result, depth_level)
            
            return {
                'depth_level': depth_level,
                'patterns': patterns,
                'meta': {
                    'depth_features': self.depth_levels[depth_level]['features'],
                    'processing_role': self.depth_levels[depth_level]['role']
                }
            }
            
        except Exception as e:
            print(colored(f"Error in depth processing: {str(e)}", "red"))
            return {
                'error': str(e),
                'depth_level': depth_level
            }

    def _create_depth_agent(self, depth_level: str) -> CognitiveAgent:
        """Create agent specialized for specific depth."""
        depth_config = self.depth_levels[depth_level]
        agent_role = f"Depth Analyst ({depth_level})"
        
        # Map depth to numeric level
        depth_map = {
            'surface': 1,
            'intermediate': 2,
            'deep': 3
        }
        
        return CognitiveAgent(
            role=agent_role,
            depth=depth_map[depth_level],
            max_depth=3
        )

    def _enhance_for_depth(
        self, 
        thought: str, 
        depth_level: str,
        context: Optional[Dict]
    ) -> str:
        """Enhance thought with depth-specific context."""
        depth_prompts = {
            'surface': "Identify immediate patterns in:",
            'intermediate': "Analyze connections and context in:",
            'deep': "Synthesize meta-patterns and systemic insights from:"
        }
        
        base_prompt = depth_prompts[depth_level]
        
        if context:
            context_str = f"\nContext: {context}"
            return f"{base_prompt} {thought}{context_str}"
        
        return f"{base_prompt} {thought}"

    def _extract_depth_patterns(self, result: Dict, depth_level: str) -> List[Dict]:
        """Extract patterns relevant to current depth level."""
        try:
            all_patterns = result.get('insights', {}).get('patterns', [])
            
            # Filter based on depth requirements
            depth_requirements = {
                'surface': lambda p: self._is_surface_pattern(p),
                'intermediate': lambda p: self._is_connection_pattern(p),
                'deep': lambda p: self._is_meta_pattern(p)
            }
            
            return [
                pattern for pattern in all_patterns 
                if depth_requirements[depth_level](pattern)
            ]
            
        except Exception as e:
            print(colored(f"Error extracting patterns: {str(e)}", "yellow"))
            return []

    def _is_surface_pattern(self, pattern: str) -> bool:
        """Check if pattern is surface-level."""
        surface_indicators = [
            'immediate', 'obvious', 'direct', 'visible',
            'clear', 'explicit', 'apparent'
        ]
        return any(indicator in pattern.lower() for indicator in surface_indicators)

    def _is_connection_pattern(self, pattern: str) -> bool:
        """Check if pattern represents connections."""
        connection_indicators = [
            'connects', 'relates', 'links', 'between',
            'association', 'correlation', 'relationship'
        ]
        return any(indicator in pattern.lower() for indicator in connection_indicators)

    def _is_meta_pattern(self, pattern: str) -> bool:
        """Check if pattern is meta-level."""
        meta_indicators = [
            'meta', 'systemic', 'underlying', 'fundamental',
            'core', 'essential', 'archetypal'
        ]
        return any(indicator in pattern.lower() for indicator in meta_indicators) 