"""OpenAI client wrapper with enhanced error handling and retries."""
from typing import Dict, Any, Optional
from termcolor import colored
import os
import json
import asyncio
from openai import AsyncOpenAI as BaseAsyncOpenAI
from openai import APIError, RateLimitError, APIConnectionError

class AsyncOpenAI(BaseAsyncOpenAI):
    """Enhanced OpenAI client with better error handling and retries."""
    
    def __init__(self, *args, **kwargs):
        # Use environment variable if no key provided
        if 'api_key' not in kwargs:
            kwargs['api_key'] = os.getenv('OPENAI_API_KEY')
            
        if not kwargs.get('api_key'):
            raise ValueError("OpenAI API key not found in environment")
            
        super().__init__(*args, **kwargs)
        self.retry_limit = 3
        self.base_delay = 1  # seconds

    async def chat_with_retries(
        self,
        messages: list,
        model: str = "gpt-4o-mini-2024-07-18",
        temperature: float = 0.7,
        response_format: Optional[Dict] = None,
        timeout: float = 30.0,
        **kwargs
    ) -> Dict[str, Any]:
        """Enhanced chat completion with retries and error handling."""
        attempt = 0
        last_error = None
        
        while attempt < self.retry_limit:
            try:
                async with asyncio.timeout(timeout):
                    response = await self.chat.completions.create(
                        model=model,
                        messages=messages,
                        temperature=temperature,
                        response_format=response_format or {"type": "json_object"},
                        **kwargs
                    )
                    
                    return json.loads(response.choices[0].message.content)
                    
            except asyncio.TimeoutError:
                print(colored(f"Request timeout (Attempt {attempt + 1})", "yellow"))
                await asyncio.sleep(self.base_delay * (2 ** attempt))
                
            except Exception as e:
                print(colored(f"Error in chat request: {str(e)}", "red"))
                if isinstance(e, RateLimitError):
                    await asyncio.sleep(self.base_delay * (2 ** attempt))
                else:
                    raise
                    
            attempt += 1
            
        raise last_error or Exception("Max retries exceeded")

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close() 