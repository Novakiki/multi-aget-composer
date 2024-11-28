from fastapi import FastAPI
from cognitive_agents import CognitiveAgent

app = FastAPI()

@app.post("/process")
async def process_thought(thought: str):
    agent = CognitiveAgent("API Observer")
    return await agent.process_thought(thought) 