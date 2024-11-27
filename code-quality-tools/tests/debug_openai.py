"""Debug OpenAI API integration."""

import asyncio
import os
from openai import AsyncOpenAI
from termcolor import colored

async def test_openai():
    """Test OpenAI API directly."""
    client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Simple test message
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use faster model for testing
        messages=[{
            "role": "user",
            "content": "Return this exact JSON: {\"test\": true}"
        }],
        temperature=0,
        response_format={"type": "json_object"}
    )
    
    print("\nResponse object:", type(response))
    print("\nMessage content:", response.choices[0].message.content)
    
    # Try parsing
    try:
        import json
        result = json.loads(response.choices[0].message.content)
        print("\nParsed JSON:", result)
    except Exception as e:
        print("\nParsing error:", str(e))

if __name__ == "__main__":
    print(colored("\nTesting OpenAI API...", "cyan"))
    asyncio.run(test_openai()) 