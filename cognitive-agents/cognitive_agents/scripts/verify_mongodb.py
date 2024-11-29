import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from termcolor import colored

async def verify_mongodb():
    """Verify MongoDB connection."""
    try:
        client = AsyncIOMotorClient("mongodb://localhost:27017")
        await client.admin.command('ping')
        print(colored("✅ MongoDB Connected", "green"))
    except Exception as e:
        print(colored(f"❌ MongoDB Error: {str(e)}", "red"))

if __name__ == "__main__":
    asyncio.run(verify_mongodb()) 