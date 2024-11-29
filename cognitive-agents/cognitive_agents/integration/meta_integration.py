from typing import Dict, List
from datetime import datetime
from termcolor import colored
from cognitive_agents.memory.meta_learning import MetaLearning

class MetaIntegration:
    """Integrates meta-learning with core system."""
    
    def __init__(self, memory, questions, community):
        self.memory = memory
        self.questions = questions
        self.community = community
        self.meta = MetaLearning()
        
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
            # Calculate evolution strength
            connection_strength = len(connections) / 5.0  # Normalize
            emergence_strength = len(emergence) / 3.0     # Normalize
            
            # Determine evolution stage
            if connection_strength > 0.7 and emergence_strength > 0.7:
                stage = 'established'
            elif connection_strength > 0.3 or emergence_strength > 0.3:
                stage = 'developing'
            else:
                stage = 'emerging'
                
            # Log evolution components
            print(colored("\n🌱 Evolution Components:", "cyan"))
            print(f"  • Connection Strength: {connection_strength:.2f}")
            print(f"  • Emergence Strength: {emergence_strength:.2f}")
            print(f"  • Evolution Stage: {stage}")
            
            return {
                'stage': stage,
                'connection_strength': connection_strength,
                'emergence_strength': emergence_strength,
                'patterns': [
                    pattern for e in emergence 
                    for pattern in e.get('patterns', [])
                ]
            }
            
        except Exception as e:
            print(colored(f"❌ Evolution error: {str(e)}", "red"))
            return {
                'stage': 'emerging',
                'connection_strength': 0,
                'emergence_strength': 0,
                'patterns': []
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