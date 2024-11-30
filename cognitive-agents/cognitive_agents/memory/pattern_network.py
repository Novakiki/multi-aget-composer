from typing import Dict
import neo4j
from termcolor import colored

class PatternNetwork:
    """Knowledge network for pattern evolution."""
    
    def __init__(self, uri: str, user: str, password: str):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = None
        
    async def connect(self):
        try:
            self.driver = neo4j.AsyncGraphDatabase.driver(
                self.uri, 
                auth=(self.user, self.password)
            )
            print(colored("✓ Connected to Neo4j", "green"))
            return True
        except Exception as e:
            print(colored(f"✗ Neo4j connection failed: {str(e)}", "red"))
            return False

    async def connect_pattern(self, pattern_id: str, pattern: Dict) -> bool:
        try:
            if not self.driver:
                print(colored("✗ No Neo4j connection", "red"))
                return False

            async with self.driver.session() as session:
                # Create pattern node
                query = """
                MERGE (p:Pattern {id: $pattern_id})
                SET p.content = $content,
                    p.type = $type
                RETURN p
                """
                
                params = {
                    "pattern_id": pattern_id,
                    "content": pattern["content"],
                    "type": pattern["type"]
                }

                result = await session.run(query, params)
                await result.consume()

                # Create theme relationships
                if "themes" in pattern:
                    for theme in pattern["themes"]:
                        theme_query = """
                        MATCH (p:Pattern {id: $pattern_id})
                        MERGE (t:Theme {name: $theme})
                        MERGE (p)-[:HAS_THEME]->(t)
                        """
                        theme_params = {
                            "pattern_id": pattern_id,
                            "theme": theme
                        }
                        result = await session.run(theme_query, theme_params)
                        await result.consume()

                print(colored(f"✓ Pattern {pattern_id} connected successfully", "green"))
                return True

        except Exception as e:
            print(colored(f"✗ Failed to connect pattern: {str(e)}", "red"))
            return False

    async def close(self):
        if self.driver:
            await self.driver.close()