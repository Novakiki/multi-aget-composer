from typing import Dict, List
from datetime import datetime
from termcolor import colored
from cognitive_agents.memory.meta_learning import MetaLearning
from cognitive_agents.memory.evolution_store import EvolutionStore

class MetaIntegration:
    """Integrates meta-learning with core system."""
    
    def __init__(self, memory, questions, community):
        self.memory = memory
        self.questions = questions
        self.community = community
        self.meta = MetaLearning()
        self.evolution_store = EvolutionStore()
        self.evolution_history = []  # Keep in-memory cache
        
    async def integrate_meta_learning(self, interaction: Dict) -> Dict:
        """Let meta-learning emerge naturally."""
        try:
            # 1. Core interaction happens
            result = await self.process_interaction(interaction)
            
            # 2. Meta-learning layer observes
            meta = await self.meta.observe_learning(interaction)
            
            # 3. Natural integration
            integrated = self._integrate_naturally(result, meta)
            
            return integrated
            
        except Exception as e:
            print(colored(f"❌ Meta integration error: {str(e)}", "red"))
            return {}
            
    def _integrate_naturally(self, core: Dict, meta: Dict) -> Dict:
        """Let meta-learning integrate without forcing."""
        try:
            # Find natural connections
            connections = self._find_connections(core, meta)
            
            # Notice what's emerging
            emergence = self._notice_emergence(core, meta)
            
            # Allow natural evolution
            evolution = self._allow_evolution(connections, emergence)
            
            # Calculate integration quality
            quality = self._calculate_integration_quality(connections, emergence)
            
            return {
                'natural_connections': connections,  # Changed from 'connections'
                'emergence': emergence,
                'evolution': evolution,
                'integration_quality': quality
            }
            
        except Exception as e:
            print(colored(f"❌ Integration error: {str(e)}", "red"))
            return {}
        
    async def process_interaction(self, interaction: Dict) -> Dict:
        """Process core interaction."""
        try:
            if interaction.get('type') == 'question':
                print(colored("\n🔍 Processing Interaction:", "cyan"))
                print(f"  • Type: {interaction.get('type')}")
                print(f"  • Content: {interaction.get('content')}")
                print(f"  • Understanding: {interaction.get('understanding', 'None')}")
                
                # Create core patterns
                patterns = []
                
                # Question pattern
                patterns.append({
                    'type': 'question_pattern',
                    'content': interaction['content'],
                    'strength': 0.8  # Questions are important
                })
                
                # Understanding pattern if available
                if 'understanding' in interaction:
                    patterns.append({
                        'type': 'understanding_pattern',
                        'content': interaction['understanding'],
                        'strength': 0.7
                    })
                
                # Add depth to patterns
                for pattern in patterns:
                    pattern['depth'] = self._calculate_pattern_depth(pattern)
                    print(colored("\n📝 Pattern Created:", "cyan"))
                    print(f"  • Type: {pattern['type']}")
                    print(f"  • Content: {pattern['content']}")
                    print(f"  • Depth: {pattern['depth']:.2f}")
                
                return {
                    'type': 'core_patterns',
                    'patterns': patterns
                }
                
            return {}
            
        except Exception as e:
            print(colored(f"❌ Process error: {str(e)}", "red"))
            return {}
        
    def _find_connections(self, core: Dict, meta: Dict) -> List[Dict]:
        """Find natural connections."""
        try:
            print(colored("\n🔗 Finding Connections:", "cyan"))
            print(f"  • Core Patterns: {len(core.get('patterns', []))}")
            print(f"  • Meta Patterns: {len(meta.get('patterns', []))}")
            
            connections = []
            core_patterns = core.get('patterns', [])
            meta_patterns = meta.get('patterns', [])
            
            # Add pattern type if missing
            for pattern in core_patterns:
                if 'type' not in pattern:
                    pattern['type'] = 'core_pattern'
                print(f"\n  Core Pattern:")
                print(f"    Content: {pattern.get('content')}")
                print(f"    Type: {pattern.get('type')}")
                print(f"    Depth: {pattern.get('depth', 0):.2f}")
            
            for pattern in meta_patterns:
                if 'type' not in pattern:
                    pattern['type'] = 'meta_pattern'
                print(f"\n  Meta Pattern:")
                print(f"    Content: {pattern.get('content')}")
                print(f"    Type: {pattern.get('type')}")
                print(f"    Depth: {pattern.get('depth', 0):.2f}")
            
            # Find connections with improved matching
            for cp in core_patterns:
                for mp in meta_patterns:
                    strength = self._calculate_connection_strength(cp, mp)
                    if strength > 0.2:  # Minimum threshold
                        connections.append({
                            'type': 'natural',
                            'core': cp,
                            'meta': mp,
                            'strength': strength
                        })
                        print(f"\n  Connection Found:")
                        print(f"    Core: {cp.get('content')}")
                        print(f"    Meta: {mp.get('content')}")
                        print(f"    Strength: {strength:.2f}")
            
            return connections
            
        except Exception as e:
            print(colored(f"❌ Connection finding error: {str(e)}", "red"))
            return []
        
    def _calculate_connection_strength(self, p1: Dict, p2: Dict) -> float:
        """Calculate connection strength between patterns."""
        try:
            # Word overlap
            words1 = set(p1.get('content', '').lower().split())
            words2 = set(p2.get('content', '').lower().split())
            overlap = len(words1.intersection(words2))
            
            # Base strength from word overlap
            base_strength = overlap / (len(words1) + len(words2) - overlap)  # Jaccard similarity
            
            # Theme matching
            themes1 = self._extract_themes(p1.get('content', '').lower())
            themes2 = self._extract_themes(p2.get('content', '').lower())
            theme_overlap = len(themes1.intersection(themes2))
            theme_strength = theme_overlap / max(len(themes1), len(themes2)) if themes1 and themes2 else 0
            
            # Combined strength
            strength = (base_strength * 0.6) + (theme_strength * 0.4)
            
            # Boost for related patterns
            if p1.get('type') == p2.get('type'):
                strength *= 1.2
                
            return min(1.0, strength)
            
        except Exception as e:
            print(colored(f"❌ Connection strength error: {str(e)}", "red"))
            return 0.0
            
    def _extract_themes(self, content: str) -> set:
        """Extract themes from content."""
        themes = set()
        if 'learn' in content: themes.add('learning')
        if 'pattern' in content: themes.add('patterns')
        if 'practice' in content or 'apply' in content: themes.add('application')
        if 'understand' in content or 'concept' in content: themes.add('understanding')
        return themes
        
    def _notice_emergence(self, core: Dict, meta: Dict) -> List[Dict]:
        """Notice what's emerging naturally."""
        try:
            # Combine patterns
            all_patterns = core.get('patterns', []) + meta.get('patterns', [])
            
            # Group by theme
            themes = self._group_by_theme(all_patterns)
            
            return [{
                'type': 'emergence',
                'theme': theme,
                'patterns': patterns,
                'strength': self._calculate_emergence_strength(patterns)
            } for theme, patterns in themes.items()]
            
        except Exception as e:
            print(colored(f"❌ Emergence error: {str(e)}", "red"))
            return []
        
    def _allow_evolution(self, connections: List[Dict], emergence: List[Dict]) -> Dict:
        """Allow natural evolution of patterns and insights."""
        try:
            # Calculate evolution metrics
            connection_strength = len(connections) / 5.0
            emergence_strength = len(emergence) / 3.0
            
            # Calculate theme coverage
            themes = set()
            for e in emergence:
                if isinstance(e.get('theme'), str):
                    themes.add(e['theme'])
            theme_coverage = len(themes) / 4.0
            
            # Calculate depth progression
            depths = []
            for conn in connections:
                depths.extend([
                    conn['core'].get('depth', 0),
                    conn['meta'].get('depth', 0)
                ])
            avg_depth = sum(depths) / len(depths) if depths else 0
            
            # Record current state
            current_state = {
                'timestamp': datetime.now().isoformat(),
                'metrics': {
                    'connection_strength': connection_strength,
                    'emergence_strength': emergence_strength,
                    'theme_coverage': theme_coverage,
                    'depth': avg_depth
                },
                'themes': list(themes),
                'pattern_count': len(connections)
            }
            
            # Determine stage with history context
            if len(self.evolution_history) == 0:
                stage = 'emerging'  # Always start at emerging
            else:
                prev_state = self.evolution_history[-1]
                # Boost scores if showing consistent growth
                if current_state['metrics']['depth'] > prev_state['metrics']['depth']:
                    avg_depth *= 1.1
                if len(current_state['themes']) > len(prev_state['themes']):
                    theme_coverage *= 1.1
                
                # Progressive stages
                if connection_strength > 0.8 and emergence_strength > 0.8 and theme_coverage > 0.8:
                    stage = 'evolving'
                elif connection_strength > 0.6 and emergence_strength > 0.6 and avg_depth > 0.7:
                    stage = 'established'
                elif connection_strength > 0.4 or (emergence_strength > 0.5 and theme_coverage > 0.5):
                    stage = 'developing'
                elif connection_strength > 0.2 or emergence_strength > 0.3:
                    stage = 'connecting'
                else:
                    stage = 'emerging'
                
            # Update state with stage
            current_state['stage'] = stage
            
            # Store in database
            self.evolution_store.store_evolution_state(current_state)
            
            # Keep in-memory cache
            self.evolution_history = self.evolution_store.get_evolution_history(limit=10)
            
            # Analyze progression
            progression = self._analyze_evolution_progression()
            
            # Enhanced logging
            print(colored("\n📈 Evolution History:", "cyan"))
            print(f"  • History Length: {len(self.evolution_history)}")
            print(f"  • Stage Changes: {progression['stage_changes']}")
            print(f"  • Growth Rate: {progression['growth_rate']:.2f}")
            print(f"  • Trend: {progression['trend']}")
            
            return {
                'stage': stage,
                'connection_strength': connection_strength,
                'emergence_strength': emergence_strength,
                'theme_coverage': theme_coverage,
                'depth': avg_depth,
                'patterns': [p for e in emergence for p in e.get('patterns', [])],
                'themes': list(themes),
                'progression': progression
            }
            
        except Exception as e:
            print(colored(f"❌ Evolution error: {str(e)}", "red"))
            return {
                'stage': 'emerging',
                'connection_strength': 0,
                'emergence_strength': 0,
                'theme_coverage': 0,
                'depth': 0,
                'patterns': [],
                'themes': [],
                'progression': {
                    'stage_changes': 0,
                    'growth_rate': 0.0,
                    'trend': 'error'
                }
            }
        
    def _calculate_integration_quality(self, connections: List[Dict], emergence: List[Dict]) -> float:
        """Calculate the quality of integration."""
        try:
            # Connection quality
            connection_quality = len(connections) / 5.0  # Normalize
            
            # Emergence quality
            emergence_quality = len(emergence) / 3.0  # Normalize
            
            # Combined quality score
            quality = (connection_quality * 0.6) + (emergence_quality * 0.4)
            
            # Log quality components
            print(colored("\n📊 Integration Quality:", "cyan"))
            print(f"  • Connection Quality: {connection_quality:.2f}")
            print(f"  • Emergence Quality: {emergence_quality:.2f}")
            print(f"  • Overall Quality: {quality:.2f}")
            
            return min(1.0, quality)
            
        except Exception as e:
            print(colored(f"❌ Quality calculation error: {str(e)}", "red"))
            return 0.0
        
    def _group_by_theme(self, patterns: List[Dict]) -> Dict[str, List[Dict]]:
        """Group patterns by common themes."""
        try:
            themes = {}
            
            for pattern in patterns:
                content = pattern.get('content', '').lower()
                
                # Extract key themes
                if 'learn' in content:
                    self._add_to_theme(themes, 'learning', pattern)
                if 'pattern' in content:
                    self._add_to_theme(themes, 'patterns', pattern)
                if 'practice' in content or 'apply' in content:
                    self._add_to_theme(themes, 'application', pattern)
                if 'understand' in content or 'concept' in content:
                    self._add_to_theme(themes, 'understanding', pattern)
                    
            return themes
            
        except Exception as e:
            print(colored(f"❌ Theme grouping error: {str(e)}", "red"))
            return {'general': patterns}
            
    def _add_to_theme(self, themes: Dict[str, List[Dict]], theme: str, pattern: Dict):
        """Add pattern to theme group."""
        if theme not in themes:
            themes[theme] = []
        themes[theme].append(pattern)
        
    def _calculate_emergence_strength(self, patterns: List[Dict]) -> float:
        """Calculate the strength of emergent patterns."""
        try:
            if not patterns:
                return 0.0
                
            # Average pattern strength
            strengths = [p.get('strength', 0) for p in patterns]
            avg_strength = sum(strengths) / len(strengths)
            
            # Adjust for pattern count
            count_factor = min(1.0, len(patterns) / 3.0)
            
            # Combined strength
            strength = avg_strength * count_factor
            
            return min(1.0, strength)
            
        except Exception as e:
            print(colored(f"❌ Emergence strength error: {str(e)}", "red"))
            return 0.0
        
    def _calculate_pattern_depth(self, pattern: Dict) -> float:
        """Calculate the depth of a pattern."""
        try:
            content = pattern.get('content', '').lower()
            depth_score = 0.0
            
            # Base depth from content length
            words = content.split()
            depth_score += min(1.0, len(words) / 10.0)
            
            # Context depth
            if pattern.get('context_depth') == 'understanding':
                depth_score *= 1.3
                
            # Question depth
            if '?' in content:
                depth_score *= 1.2
                
            # Concept markers
            understanding_words = {'because', 'therefore', 'thus', 'hence', 'through', 'involves'}
            if any(word in content for word in understanding_words):
                depth_score *= 1.25
                
            # Theme depth
            themes = []
            if 'learn' in content: themes.append('learning')
            if 'pattern' in content: themes.append('patterns')
            if 'practice' in content or 'apply' in content: themes.append('application')
            if 'understand' in content or 'concept' in content: themes.append('understanding')
            
            # Adjust for theme coverage
            theme_factor = min(1.0, len(themes) / 3.0)
            depth_score *= (1.0 + theme_factor)
            
            # Log depth calculation
            print(colored("\n📏 Pattern Depth:", "cyan"))
            print(f"  • Content: {content}")
            print(f"  • Themes: {', '.join(themes)}")
            print(f"  • Final Depth: {min(1.0, depth_score):.2f}")
            
            return min(1.0, depth_score)
            
        except Exception as e:
            print(colored(f"❌ Pattern depth calculation error: {str(e)}", "red"))
            return 0.0
        
    def _analyze_evolution_progression(self) -> Dict:
        """Analyze how evolution has progressed over time."""
        try:
            if not self.evolution_history:
                return {
                    'stage_changes': 0,
                    'growth_rate': 0.0,
                    'trend': 'initial'
                }
            
            # Count stage changes
            stage_changes = sum(
                1 for i in range(1, len(self.evolution_history))
                if self.evolution_history[i]['stage'] != self.evolution_history[i-1]['stage']
            )
            
            # Calculate growth rate from metrics
            if len(self.evolution_history) >= 2:
                current = self.evolution_history[0]['metrics']  # Most recent first
                previous = self.evolution_history[1]['metrics']
                
                # Weight the metrics differently
                growth_factors = [
                    (current['connection_strength'] - previous['connection_strength']) * 0.3,
                    (current['emergence_strength'] - previous['emergence_strength']) * 0.3,
                    (current['theme_coverage'] - previous['theme_coverage']) * 0.2,
                    (current['depth'] - previous['depth']) * 0.2
                ]
                
                # Add bonus for stage progression
                if stage_changes > 0:
                    growth_bonus = 0.2
                else:
                    growth_bonus = 0
                    
                growth_rate = sum(growth_factors) + growth_bonus
            else:
                growth_rate = 0.0
                
            # Determine trend
            if growth_rate > 0.1:
                trend = 'accelerating'
            elif growth_rate < -0.1:
                trend = 'consolidating'
            else:
                trend = 'stable'
                
            return {
                'stage_changes': stage_changes,
                'growth_rate': growth_rate,
                'trend': trend
            }
            
        except Exception as e:
            print(colored(f"❌ Progression analysis error: {str(e)}", "red"))
            return {
                'stage_changes': 0,
                'growth_rate': 0.0,
                'trend': 'error'
            }