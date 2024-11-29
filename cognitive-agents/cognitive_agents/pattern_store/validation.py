from typing import Dict, List, Optional
from datetime import datetime, timedelta
from termcolor import colored
import asyncio

class CommunityValidation:
    """Community-driven pattern validation system."""
    
    def __init__(self):
        self.active_validations = {}
        self.validation_results = {}
        
    async def initiate_validation(
        self,
        pattern_id: str,
        validators: List[str]
    ) -> Dict:
        """Start community validation process for a pattern."""
        try:
            validation = {
                'pattern_id': pattern_id,
                'status': 'active',
                'phases': {
                    'personal_testing': {
                        'required_validators': 5,
                        'duration_days': 7,
                        'results': []
                    },
                    'group_testing': {
                        'required_groups': 2,
                        'duration_days': 14,
                        'results': []
                    },
                    'real_world': {
                        'required_cases': 10,
                        'duration_days': 30,
                        'results': []
                    }
                },
                'started_at': datetime.now(),
                'validators': validators
            }
            
            print(colored(f"\n Starting validation for pattern: {pattern_id}", "cyan"))
            return validation
            
    async def submit_validation_result(
        self,
        pattern_id: str,
        validator_id: str,
        phase: str,
        result: Dict
    ) -> bool:
        """Submit validation results from community testing."""
        try:
            validation_data = {
                'validator_id': validator_id,
                'timestamp': datetime.now().isoformat(),
                'phase': phase,
                'result': {
                    'effectiveness': result.get('effectiveness', 0.0),
                    'applicability': result.get('applicability', 0.0),
                    'evidence': result.get('evidence', []),
                    'feedback': result.get('feedback', ''),
                    'suggested_improvements': result.get('improvements', [])
                }
            }
            
            # Store validation result
            await self.db.execute(
                """
                INSERT INTO validation_results (
                    pattern_id,
                    phase,
                    result_data
                ) VALUES (?, ?, ?)
                """,
                (pattern_id, phase, validation_data)
            )
            
            # Check phase completion
            await self._check_phase_completion(pattern_id, phase)
            
            return True
            
        except Exception as e:
            print(colored(f"❌ Error submitting validation: {str(e)}", "red"))
            return False
            
    async def get_validation_status(
        self,
        pattern_id: str
    ) -> Dict:
        """Get current validation status and results."""
        try:
            results = await self.db.execute(
                """
                SELECT phase, result_data
                FROM validation_results
                WHERE pattern_id = ?
                ORDER BY result_data->>'timestamp'
                """,
                (pattern_id,)
            )
            
            status = {
                'personal_testing': {
                    'completed': 0,
                    'average_effectiveness': 0.0,
                    'feedback': []
                },
                'group_testing': {
                    'completed': 0,
                    'average_effectiveness': 0.0,
                    'feedback': []
                },
                'real_world': {
                    'completed': 0,
                    'average_effectiveness': 0.0,
                    'feedback': []
                }
            }
            
            # Process results
            for phase, result in results:
                status[phase]['completed'] += 1
                status[phase]['average_effectiveness'] += result['effectiveness']
                if result.get('feedback'):
                    status[phase]['feedback'].append(result['feedback'])
                    
            return status
            
        except Exception as e:
            print(colored(f"❌ Error getting validation status: {str(e)}", "red"))
            return {}
            
    async def _check_phase_completion(
        self,
        pattern_id: str,
        phase: str
    ):
        """Check if validation phase is complete."""
        status = await self.get_validation_status(pattern_id)
        phase_status = status[phase]
        
        if self._is_phase_complete(phase_status):
            await self._advance_validation_phase(pattern_id)
            
    def _is_phase_complete(self, phase_status: Dict) -> bool:
        """Check if phase meets completion criteria."""
        required_counts = {
            'personal_testing': 5,
            'group_testing': 2,
            'real_world': 10
        }
        
        return (
            phase_status['completed'] >= required_counts[phase_status] and
            phase_status['average_effectiveness'] >= 0.8
        ) 