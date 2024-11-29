from typing import Dict, List, Optional
from termcolor import colored
import asyncio

from .vertical_processor import VerticalProcessor
from .cognitive_agent import CognitiveAgent

class CognitiveOrchestrator:
    """Orchestrates multi-dimensional agent processing."""
    
    def __init__(self):
        self.vertical_processor = VerticalProcessor()
        self.active_agents = {}  # Track active agents
        print(colored("🎭 Cognitive Orchestrator initialized", "green"))

    async def process_thought(self, thought: str) -> Dict:
        """Process thought across all dimensions."""
        try:
            print(colored("\n🔄 Starting multi-dimensional processing", "cyan"))
            
            # 1. Start with vertical processing
            vertical_results = await self._process_vertical(thought)
            
            # 2. Track spawned agents
            self._update_active_agents(vertical_results)
            
            # 3. Monitor and manage agent lifecycle
            await self._monitor_agents()
            
            # 4. Integrate results
            integrated_results = await self._integrate_results(vertical_results)
            
            return integrated_results
            
        except Exception as e:
            print(colored(f"❌ Orchestration error: {str(e)}", "red"))
            return {"error": str(e)}

    async def _process_vertical(self, thought: str) -> Dict:
        """Process through vertical depth levels."""
        try:
            # Process at all depths concurrently
            results = await asyncio.gather(
                self.vertical_processor.process_at_depth(thought, 'surface'),
                self.vertical_processor.process_at_depth(thought, 'intermediate'),
                self.vertical_processor.process_at_depth(thought, 'deep')
            )
            
            print(colored(f"\n📊 Vertical processing complete", "green"))
            print(f"  • Surface patterns: {len(results[0].get('patterns', []))}")
            print(f"  • Intermediate patterns: {len(results[1].get('patterns', []))}")
            print(f"  • Deep patterns: {len(results[2].get('patterns', []))}")
            
            return {
                'surface': results[0],
                'intermediate': results[1],
                'deep': results[2]
            }
            
        except Exception as e:
            print(colored(f"Error in vertical processing: {str(e)}", "red"))
            return {}

    def _update_active_agents(self, results: Dict):
        """Track active agents across dimensions."""
        for depth, result in results.items():
            agent_id = f"vertical_{depth}"
            self.active_agents[agent_id] = {
                'type': 'vertical',
                'depth': depth,
                'status': 'active',
                'patterns_found': len(result.get('patterns', []))
            }

    async def _monitor_agents(self):
        """Monitor and manage agent lifecycle."""
        try:
            for agent_id, info in self.active_agents.items():
                print(colored(f"\n👁️  Monitoring agent: {agent_id}", "cyan"))
                print(f"  • Type: {info['type']}")
                print(f"  • Depth: {info['depth']}")
                print(f"  • Status: {info['status']}")
                print(f"  • Patterns: {info['patterns_found']}")
                
        except Exception as e:
            print(colored(f"Error monitoring agents: {str(e)}", "yellow"))

    async def _integrate_results(self, vertical_results: Dict) -> Dict:
        """Integrate results across dimensions."""
        try:
            all_patterns = []
            meta_insights = []
            
            # Collect patterns from all depths
            for depth, result in vertical_results.items():
                patterns = result.get('patterns', [])
                all_patterns.extend(patterns)
                
                # Extract meta information
                meta = result.get('meta', {})
                meta_insights.append({
                    'depth': depth,
                    'features': meta.get('depth_features', []),
                    'role': meta.get('processing_role', '')
                })
            
            return {
                'integrated_results': {
                    'patterns': all_patterns,
                    'meta_insights': meta_insights,
                    'dimensions_processed': {
                        'vertical': True,
                        'horizontal': False,  # Coming soon
                        'diagonal': False     # Coming soon
                    }
                },
                'agent_status': self.active_agents
            }
            
        except Exception as e:
            print(colored(f"Error integrating results: {str(e)}", "red"))
            return {} 