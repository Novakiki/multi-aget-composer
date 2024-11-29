from typing import Dict, List, Optional
from datetime import datetime
from termcolor import colored
import asyncio

from .db import PatternStore
from ..config import PATTERN_SETTINGS, VALIDATION_THRESHOLDS

class CommunityPatternStore(PatternStore):
    """Extended pattern store with community governance."""
    
    def __init__(self):
        super().__init__()
        self.voting_cache = {}
        self.pattern_status = {}
    
    async def store_pattern_proposal(
        self, 
        pattern: Dict,
        proposer_id: str
    ) -> str:
        """Store new pattern proposal for community review."""
        try:
            # Initial validation
            if not self._meets_basic_criteria(pattern):
                print(colored("⚠️ Pattern doesn't meet basic criteria", "yellow"))
                return None
                
            # Add metadata
            pattern_id = self._generate_pattern_id(pattern)
            pattern.update({
                'status': 'proposed',
                'proposer_id': proposer_id,
                'proposed_at': datetime.now().isoformat(),
                'votes': {
                    'up': 0,
                    'down': 0,
                    'refinements': 0,
                    'validations': 0
                }
            })
            
            # Store in review pool
            await self.db.execute(
                """
                INSERT INTO pattern_proposals (
                    pattern_id,
                    pattern_data,
                    status,
                    proposer_id,
                    proposed_at
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (pattern_id, pattern, 'proposed', proposer_id, pattern['proposed_at'])
            )
            
            print(colored(f"📝 Pattern proposal stored: {pattern_id}", "green"))
            return pattern_id
            
        except Exception as e:
            print(colored(f"❌ Error storing pattern proposal: {str(e)}", "red"))
            return None
            
    async def vote_on_pattern(
        self,
        pattern_id: str,
        voter_id: str,
        vote_type: str,
        feedback: Optional[str] = None
    ) -> bool:
        """Record a vote on a pattern proposal."""
        try:
            # Validate vote
            if not self._can_vote(voter_id, pattern_id):
                return False
                
            # Record vote
            vote = {
                'voter_id': voter_id,
                'vote_type': vote_type,
                'feedback': feedback,
                'timestamp': datetime.now().isoformat()
            }
            
            await self.db.execute(
                """
                INSERT INTO pattern_votes (
                    pattern_id,
                    vote_data
                ) VALUES (?, ?)
                """,
                (pattern_id, vote)
            )
            
            # Update pattern status
            await self._check_pattern_status(pattern_id)
            
            return True
            
        except Exception as e:
            print(colored(f"❌ Error recording vote: {str(e)}", "red"))
            return False
            
    async def _check_pattern_status(self, pattern_id: str):
        """Check if pattern meets criteria for status change."""
        votes = await self._get_pattern_votes(pattern_id)
        
        # Calculate scores
        score = self._calculate_pattern_score(votes)
        
        # Check thresholds
        for status, threshold in VALIDATION_THRESHOLDS.items():
            if self._meets_threshold(score, threshold):
                await self._update_pattern_status(pattern_id, status)
                break 