import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")


async def call_tool(name: str):
    try:
        async with client:
            result = await client.call_tool("greet", {"name": name})
            # Handle the CallToolResult object
            if hasattr(result, 'content'):
                # If result has content attribute, print the values
                for item in result.content:
                    if hasattr(item, 'text'):
                        print(item.text)
                    else:
                        print(item)
            else:
                print(result)
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(call_tool("Ford"))
