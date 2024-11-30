import pytest
from cognitive_agents.core.event_bus import EventBus

@pytest.mark.asyncio
async def test_event_publishing():
    """Test basic event publishing and subscribing."""
    bus = EventBus()
    received_events = []
    
    # Create test subscriber
    async def test_subscriber(data):
        received_events.append(data)
    
    # Subscribe and publish
    bus.subscribe('test.event', test_subscriber)
    await bus.publish('test.event', {'message': 'test'})
    
    # Verify
    assert len(received_events) == 1
    assert received_events[0]['message'] == 'test'

@pytest.mark.asyncio
async def test_multiple_subscribers():
    """Test multiple subscribers for same event."""
    bus = EventBus()
    count_1 = 0
    count_2 = 0
    
    # Create test subscribers
    async def subscriber_1(data):
        nonlocal count_1
        count_1 += 1
    
    async def subscriber_2(data):
        nonlocal count_2
        count_2 += 1
    
    # Subscribe both and publish
    bus.subscribe('test.event', subscriber_1)
    bus.subscribe('test.event', subscriber_2)
    await bus.publish('test.event', {'message': 'test'})
    
    # Verify both received event
    assert count_1 == 1
    assert count_2 == 1

@pytest.mark.asyncio
async def test_event_history():
    """Test event history tracking."""
    bus = EventBus()
    
    # Publish some events
    await bus.publish('test.event', {'id': 1})
    await bus.publish('other.event', {'id': 2})
    await bus.publish('test.event', {'id': 3})
    
    # Get history
    all_history = bus.get_event_history()
    test_history = bus.get_event_history('test.event')
    
    # Verify
    assert len(all_history) == 3
    assert len(test_history) == 2
    assert test_history[0]['data']['id'] == 1
    assert test_history[1]['data']['id'] == 3

@pytest.mark.asyncio
async def test_unsubscribe():
    """Test unsubscribing from events."""
    bus = EventBus()
    received_events = []
    
    # Create test subscriber
    async def test_subscriber(data):
        received_events.append(data)
    
    # Subscribe, publish, unsubscribe, publish again
    bus.subscribe('test.event', test_subscriber)
    await bus.publish('test.event', {'count': 1})
    bus.unsubscribe('test.event', test_subscriber)
    await bus.publish('test.event', {'count': 2})
    
    # Verify only first event was received
    assert len(received_events) == 1
    assert received_events[0]['count'] == 1 