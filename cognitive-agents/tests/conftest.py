import pytest
import asyncio
from typing import AsyncGenerator
import pytest_asyncio

@pytest.fixture(scope="session")
def event_loop_policy():
    """Fixture that provides the event loop policy."""
    return asyncio.get_event_loop_policy()

@pytest_asyncio.fixture(scope="function")
async def event_loop(event_loop_policy) -> AsyncGenerator[asyncio.AbstractEventLoop, None]:
    """Create and provide an event loop for each test case.
    
    This fixture uses the event_loop_policy fixture to create loops,
    ensuring proper cleanup and avoiding loop leaks.
    """
    loop = event_loop_policy.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        yield loop
    finally:
        if loop.is_running():
            loop.stop()
        if not loop.is_closed():
            loop.close()
        asyncio.set_event_loop(None)

@pytest.fixture(scope="session")
async def test_db():
    """Create test database connection."""
    try:
        # Setup would go here
        yield
    finally:
        # Teardown would go here
        pass