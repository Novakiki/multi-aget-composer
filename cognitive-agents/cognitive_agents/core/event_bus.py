from typing import Dict, Callable, List, Any, Optional
from termcolor import colored
import asyncio
from datetime import datetime

class EventBus:
    """
    Central event system for agent communication and coordination.
    Enables natural emergence of insights through event-driven processing.
    """
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_history: List[Dict] = []
        print(colored("🚌 Event Bus initialized", "green"))

    async def publish(self, event_type: str, data: Any) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: Type of event (e.g., 'pattern.discovered')
            data: Event payload
        """
        try:
            print(colored(f"\n📢 Publishing event: {event_type}", "cyan"))
            
            # Record event
            self.event_history.append({
                'timestamp': datetime.now().isoformat(),
                'type': event_type,
                'data': data
            })
            
            # Notify subscribers
            if event_type in self.subscribers:
                subscriber_tasks = [
                    subscriber(data) 
                    for subscriber in self.subscribers[event_type]
                ]
                await asyncio.gather(*subscriber_tasks)
                
            print(colored(f"✓ Event {event_type} processed", "green"))
            
        except Exception as e:
            print(colored(f"❌ Error publishing event: {str(e)}", "red"))

    def subscribe(self, event_type: str, callback: Callable) -> None:
        """
        Subscribe to an event type.
        
        Args:
            event_type: Type of event to subscribe to
            callback: Async function to call when event occurs
        """
        try:
            if event_type not in self.subscribers:
                self.subscribers[event_type] = []
            
            self.subscribers[event_type].append(callback)
            print(colored(f"👂 New subscriber for {event_type}", "green"))
            
        except Exception as e:
            print(colored(f"❌ Error adding subscriber: {str(e)}", "red"))

    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """
        Unsubscribe from an event type.
        
        Args:
            event_type: Type of event to unsubscribe from
            callback: Callback function to remove
        """
        try:
            if event_type in self.subscribers:
                self.subscribers[event_type].remove(callback)
                print(colored(f"🔕 Unsubscribed from {event_type}", "yellow"))
                
        except Exception as e:
            print(colored(f"❌ Error removing subscriber: {str(e)}", "red"))

    def get_event_history(self, event_type: Optional[str] = None) -> List[Dict]:
        """
        Get history of events, optionally filtered by type.
        
        Args:
            event_type: Optional type to filter by
            
        Returns:
            List of event records
        """
        if event_type:
            return [
                event for event in self.event_history 
                if event['type'] == event_type
            ]
        return self.event_history 