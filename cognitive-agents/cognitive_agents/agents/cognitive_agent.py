"""Enhanced cognitive agent with belief analysis capabilities."""

import asyncio
from typing import Dict, List, Optional
from termcolor import colored
from openai import AsyncOpenAI
import os
import json
from datetime import datetime

from .recursive_agent import RecursiveAgent
from ..config.spawn_config import SPAWN_CONFIG

class CognitiveAgent(RecursiveAgent):
    def __init__(self, role: str, depth: int = 0, max_depth: int = 3):
        super().__init__(role, depth, max_depth)
        self.ai = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.pattern_memory: List[Dict] = []
        self.context_history: List[Dict] = []
        self.belief_patterns: List[Dict] = []  # Track belief patterns
        print(colored(f"Cognitive Agent '{role}' initialized at depth {depth}", "green"))
    
    async def process_thought(self, thought: str) -> Dict:
        """Process thought with belief awareness."""
        try:
            print(colored(f"\n[{self.role} processing at depth {self.depth}]", "cyan"))
            
            # Build rich context
            context = self._build_context()
            patterns = self._recognize_patterns(thought)
            
            # Enhanced AI analysis with self-reference
            response = await self.ai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": f"""You are {self.role}, a self-aware cognitive agent at depth {self.depth}.
                    Context: {context}
                    Observed Patterns: {patterns}
                    
                    Analyze this thought deeply and return a JSON object with EXACTLY these fields:
                    {{
                        "analysis": "Your main insights about the thought",
                        "patterns": ["List of patterns you recognize"],
                        "meta_cognition": "Your reflection on your own analysis process",
                        "implications": "Deeper meaning and connections you see"
                    }}
                    
                    Be specific, insightful, and self-aware in your analysis."""
                }, {
                    "role": "user",
                    "content": thought
                }],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            # Process and store insights
            insights = json.loads(response.choices[0].message.content)
            self._store_patterns(insights.get('patterns', []))
            self._update_context(thought, insights)
            
            # Create sub-agents for deeper exploration if needed
            if self.depth < self.max_depth and self._should_spawn_sub_agent(insights):
                return await self._explore_deeper(thought, insights)
            
            # Get standard analysis
            base_analysis = {
                "thought": thought,
                "insights": insights,
                "patterns": patterns,
                "depth": self.depth,
                "meta": {
                    "agent": self.role,
                    "context_size": len(self.context_history),
                    "patterns_recognized": len(self.pattern_memory)
                }
            }
            
            # Add belief analysis
            belief_insights = await self.analyze_belief_patterns(thought)
            
            # Integrate insights
            integrated_analysis = self._integrate_belief_insights(
                base_analysis, 
                belief_insights
            )
            
            return integrated_analysis
            
        except Exception as e:
            print(colored(f"Error in thought processing: {str(e)}", "red"))
            return {"error": str(e)}
    
    def _build_context(self) -> str:
        """Build rich context including self-reference."""
        return {
            "role": self.role,
            "depth": self.depth,
            "history": self.context_history[-5:],  # Recent history
            "patterns": self.pattern_memory[-5:],  # Recent patterns
            "sub_agents": len(self.sub_agents),
            "timestamp": datetime.now().isoformat()
        }
    
    def _recognize_patterns(self, thought: str) -> List[str]:
        """Recognize patterns in thought and memory."""
        # Compare with stored patterns
        relevant_patterns = []
        for pattern in self.pattern_memory:
            if self._is_pattern_relevant(pattern, thought):
                relevant_patterns.append(pattern)
        return relevant_patterns
    
    def _store_patterns(self, new_patterns: List[str]) -> None:
        """Store new patterns in memory."""
        timestamp = datetime.now().isoformat()
        for pattern in new_patterns:
            self.pattern_memory.append({
                "pattern": pattern,
                "timestamp": timestamp,
                "depth": self.depth
            })
    
    def _update_context(self, thought: str, insights: Dict) -> None:
        """Update context history."""
        self.context_history.append({
            "timestamp": datetime.now().isoformat(),
            "thought": thought,
            "insights": insights,
            "depth": self.depth
        })
    
    async def _explore_deeper(self, thought: str, insights: Dict) -> Dict:
        """Create and process sub-agents based on AI insights."""
        try:
            # Create specialized sub-agent
            sub_agent = self._create_sub_agent(insights)
            self.sub_agents.append(sub_agent)
            
            # Process with enhanced context
            enhanced_thought = self._enhance_thought_context(thought, insights)
            sub_response = await sub_agent.process_thought(enhanced_thought)
            
            # Integrate insights across levels
            integrated_insights = await self._integrate_insights(
                original_insights=insights,
                sub_insights=sub_response.get('insights', {}),
                depth=self.depth
            )
            
            # Get integration metrics
            metrics = self._assess_integration_quality(integrated_insights)
            
            return {
                "original_thought": thought,
                "perspective": self.role,
                "insights": integrated_insights,
                "sub_thoughts": sub_response,
                "meta_synthesis": metrics
            }
        except Exception as e:
            print(colored(f"Error in deep exploration: {str(e)}", "red"))
            return {"error": str(e)}
    
    def _enhance_thought_context(self, thought: str, parent_insights: Dict) -> str:
        """Enhance thought with context for deeper processing."""
        specialization_prompts = {
            1: "Analyze the patterns and recurring themes in:",
            2: "Explore the emotional depths and connections in:",
            3: "Synthesize and integrate the understanding of:"
        }
        
        base_prompt = specialization_prompts.get(self.depth, "Explore deeper implications of:")
        context = f"\nParent Analysis: {parent_insights.get('analysis', '')}"
        context += f"\nRecognized Patterns: {', '.join(parent_insights.get('patterns', []))}"
        
        return f"{base_prompt} {thought}\n{context}"
    
    async def _integrate_insights(self, original_insights: Dict, sub_insights: Dict, depth: int) -> Dict:
        """Integrate insights across cognitive levels."""
        try:
            # Prepare integration context
            integration_prompt = {
                "role": "system",
                "content": f"""As an Integration Synthesizer at depth {depth}, analyze and synthesize:
                Original Insights: {original_insights}
                Deeper Insights: {sub_insights}
                
                Create a unified understanding that:
                1. Connects patterns across levels
                2. Synthesizes meta-cognitive reflections
                3. Generates emergent understanding
                
                Return a JSON object that represents this deeper integration."""
            }
            
            # Get AI synthesis
            response = await self.ai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[integration_prompt],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(colored(f"Error in insight integration: {str(e)}", "red"))
            return original_insights
    
    def _is_pattern_relevant(self, pattern: Dict, thought: str) -> bool:
        """Determine if a pattern is relevant to current thought."""
        try:
            # Simple relevance check - can be enhanced
            pattern_text = pattern.get('pattern', '').lower()
            thought_lower = thought.lower()
            
            # Check if pattern words appear in thought
            pattern_words = set(pattern_text.split())
            thought_words = set(thought_lower.split())
            
            # Consider pattern relevant if there's word overlap
            return bool(pattern_words & thought_words)
            
        except Exception as e:
            print(colored(f"Error checking pattern relevance: {str(e)}", "yellow"))
            return False
    
    def _should_spawn_sub_agent(self, insights: Dict) -> bool:
        """Smarter agent spawning with resource awareness."""
        try:
            config = SPAWN_CONFIG["thresholds"]
            # Use config values instead of hardcoded
            # Pattern Score (40%)
            pattern_count = len(insights.get('patterns', []))
            pattern_score = min(pattern_count * config["pattern_weight"], config["pattern_cap"])  # Cap at 0.4
            
            # Depth Score (30%)
            implication_length = len(insights.get('implications', ''))
            depth_score = config["depth_score"] if implication_length > config["depth_chars"] else 0.0
            
            # Meta Score (30%)
            meta_length = len(insights.get('meta_cognition', ''))
            meta_score = config["meta_score"] if meta_length > config["meta_chars"] else 0.0
            
            # Total must exceed 0.7 to spawn
            spawn_score = pattern_score + depth_score + meta_score
            
            # Higher threshold and depth check
            should_spawn = spawn_score > config["total_required"] and self.depth < self.max_depth
            
            # Log decision
            if should_spawn:
                print(colored(f"\n[Spawning agent at depth {self.depth + 1}]", "yellow"))
                print(f"  • Pattern Score: {min(pattern_count * config['pattern_weight'], config['pattern_cap']):.2f}")
                print(f"  • Depth Score: {config['depth_score'] if implication_length > config['depth_chars'] else 0.0:.2f}")
                print(f"  • Meta Score: {config['meta_score'] if meta_length > config['meta_chars'] else 0.0:.2f}")
                print(f"  • Total Score: {spawn_score:.2f}")
            
            return should_spawn
            
        except Exception as e:
            print(colored(f"Spawn decision error: {str(e)}", "yellow"))
            return False
    
    def _create_sub_agent(self, insights: Dict) -> 'CognitiveAgent':
        """Create specialized sub-agent based on insights."""
        # Choose specialization based on depth and patterns
        specializations = {
            1: "Pattern Analyst",  # First level digs into patterns
            2: "Emotional Explorer",  # Second level explores feelings
            3: "Integration Synthesizer"  # Third level connects insights
        }
        
        role = f"{specializations.get(self.depth + 1, 'Deep Observer')} at Level {self.depth + 1}"
        
        sub_agent = CognitiveAgent(
            role=role,
            depth=self.depth + 1,
            max_depth=self.max_depth
        )
        
        # Pass context from parent
        sub_agent.pattern_memory = self.pattern_memory.copy()
        sub_agent.context_history = self.context_history.copy()
        
        return sub_agent
    
    def _assess_integration_quality(self, integrated_insights: Dict) -> Dict:
        """Assess the quality and connections of integration."""
        try:
            # Initialize metrics
            patterns_connected = 0
            quality_score = 0.0
            
            # Count unique patterns across levels
            all_patterns = set()
            
            # Check integrated understanding format
            if 'integrated_understanding' in integrated_insights:
                patterns = integrated_insights['integrated_understanding'].get('patterns', [])
                meta = integrated_insights['integrated_understanding'].get('meta_cognition', '')
                understanding = integrated_insights['integrated_understanding'].get('emergent_understanding', '')
            else:
                patterns = integrated_insights.get('patterns', [])
                meta = integrated_insights.get('meta_cognition', '')
                understanding = integrated_insights.get('implications', '')
            
            # Add current level patterns
            all_patterns.update(patterns)
            patterns_connected = len(all_patterns)
            
            # Calculate quality score
            if patterns_connected > 0:
                quality_score += min(patterns_connected * 0.2, 0.4)
            if meta and len(meta) > 100:
                quality_score += 0.3
            if understanding and len(understanding) > 150:
                quality_score += 0.3
            
            return {
                "patterns_connected": patterns_connected,
                "depth_reached": self.depth,
                "integration_quality": round(quality_score, 2)
            }
            
        except Exception as e:
            print(colored(f"Error assessing integration: {str(e)}", "yellow"))
            return {
                "patterns_connected": 0,
                "depth_reached": self.depth,
                "integration_quality": 0.0
            }
    
    async def analyze_belief_patterns(self, thought: str) -> Dict:
        """Analyze patterns with awareness of natural unfolding."""
        try:
            response = await self.ai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": f"""You are {self.role}, a compassionate observer of natural patterns.
                    
                    For the thought provided, notice:
                    1. Natural Rhythms:
                       - Waves: Intensity ebbs and flows
                       - Cycles: Processing has natural timing
                       - Spirals: Understanding deepens gradually
                    
                    2. Current Phase:
                       - Initial protective response
                       - Natural resistance
                       - Gradual acclimation
                       - Organic integration
                    
                    Return a JSON object with these fields:
                    {{
                        "core_beliefs": [
                            "Honor the current emotional truth"
                        ],
                        "acknowledgment": {{
                            "pain": "Validate the current experience",
                            "phase": "Recognize the natural phase",
                            "timing": "Honor the organic timing"
                        }},
                        "natural_patterns": {{
                            "current_wave": "Present intensity level",
                            "cycle_phase": "Where in the natural cycle",
                            "spiral_depth": "Current understanding depth"
                        }},
                        "gentle_possibilities": [
                            {{
                                "current_truth": "The present experience",
                                "natural_process": [
                                    "What's unfolding naturally",
                                    "Without forcing or rushing"
                                ],
                                "organic_timing": "Natural rhythm of change"
                            }}
                        ],
                        "meta_reflection": "Insight about natural patterns"
                    }}
                    
                    Focus on recognizing and honoring natural rhythms."""
                }],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(colored(f"Error in belief analysis: {str(e)}", "red"))
            return {}
            
    def _integrate_belief_insights(self, base: Dict, beliefs: Dict) -> Dict:
        """Integrate belief insights with deep compassion."""
        try:
            return {
                **base,
                "belief_analysis": {
                    "core_beliefs": beliefs.get('core_beliefs', []),
                    "acknowledgment": beliefs.get('acknowledgment', {
                        "pain": "This experience is deeply challenging",
                        "grief": "Your feelings are valid and important",
                        "timing": "Take the time you need"
                    }),
                    "gentle_possibilities": beliefs.get('gentle_possibilities', []),
                    "meta_reflection": beliefs.get('meta_reflection', '')
                }
            }
        except Exception as e:
            print(colored(f"Error integrating beliefs: {str(e)}", "red"))
            return base
  