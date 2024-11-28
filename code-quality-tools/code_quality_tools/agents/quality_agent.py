"""Quality monitoring agent."""

import asyncio
from typing import Dict, Optional
from termcolor import colored
from ..quality_monitor import QualityMonitor
from .base_agent import BaseAgent

class QualityAgent(BaseAgent):
    """Agent responsible for code quality analysis."""
    
    def __init__(self):
        super().__init__("QualityAgent")
        self.monitor = QualityMonitor()
        
    async def handle_message(self, message: Dict) -> Optional[Dict]:
        """Handle incoming file change messages."""
        try:
            if message.get('type') == 'file_change':
                file_path = message.get('file_path')
                if file_path:
                    print(colored(f"\nQuality Agent analyzing: {file_path}", "cyan"))
                    results = await self.monitor.check_file(file_path)
                    return {
                        'type': 'analysis_complete',
                        'file_path': file_path,
                        'results': results
                    }
            return None
            
        except Exception as e:
            print(colored(f"Quality Agent error: {str(e)}", "red"))
            return {
                'type': 'error',
                'error': str(e)
            } 