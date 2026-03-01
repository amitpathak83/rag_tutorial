#!/usr/bin/env python3
"""
MCP Calculator Server Usage Examples
Demonstrates how to use the FastMCP Calculator server.
"""

print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                    MCP CALCULATOR - USAGE EXAMPLES                       ║
╚══════════════════════════════════════════════════════════════════════════╝

The MCP Calculator Server provides calculator tools via the Model Context Protocol.

1. START THE SERVER
   ─────────────────────────────────────────────────────────────────────────
   
   Terminal 1:
   $ python mcp_calculator_server.py
   
   This starts the FastMCP server listening on stdin/stdout.


2. CONFIGURE MCP CLIENT
   ─────────────────────────────────────────────────────────────────────────
   
   Option A: Use with Claude (claude_cli)
   
   Create .mcp-cli.json:
   {
     "mcpServers": {
       "calculator": {
         "command": "python",
         "args": ["/path/to/mcp_calculator_server.py"],
         "env": {}
       }
     }
   }
   
   Then use: claude -c /path/to/.mcp-cli.json
   
   
   Option B: Use with LangChain
   
   ```python
   from mcp.client.session import ClientSession
   from mcp.client.stdio import stdio_client, StdioServerParameters
   import asyncio
   
   async def demo():
       transport = stdio_client(
           StdioServerParameters(
               command="python",
               args=["mcp_calculator_server.py"]
           )
       )
       
       async with transport:
           session = ClientSession(transport)
           async with session:
               await session.initialize()
               result = await session.call_tool("add", {"a": 5, "b": 3})
               print(f"5 + 3 = {result.content[0].text}")
   
   asyncio.run(demo())
   ```
   
   Option C: Custom Python Client
   
   Implement the MCP protocol to communicate with the server over stdio.


3. AVAILABLE TOOLS
   ─────────────────────────────────────────────────────────────────────────
   
   add(a: float, b: float)
     Add two numbers
   
   subtract(a: float, b: float)
      Subtract b from a
   
   multiply(a: float, b: float)
     Multiply two numbers
   
   divide(a: float, b: float)
     Divide a by b
   
   power(base: float, exponent: float)
     Raise base to power
   
   square_root(n: float)
     Calculate square root
   
   percentage(value: float, percent: float)
     Calculate percentage of value
   
   modulo(a: float, b: float)
     Get remainder of a ÷ b
   
   average(*numbers: float)
     Calculate average
   
   factorial(n: int)
     Calculate factorial


4. TOOL CALL EXAMPLES
   ─────────────────────────────────────────────────────────────────────────
   
   MCP Protocol Format:
   
   Request:
   {
     "jsonrpc": "2.0",
     "id": 1,
     "method": "tools/call",
     "params": {
       "name": "add",
       "arguments": {
         "a": 5,
         "b": 3
       }
     }
   }
   
   Response:
   {
     "jsonrpc": "2.0",
     "id": 1,
     "result": {
       "content": [
         {
           "type": "text",
           "text": "8"
         }
       ],
       "isError": false
     }
   }


5. EXTENDING THE SERVER
   ─────────────────────────────────────────────────────────────────────────
   
   Add a new tool:
   
   @mcp.tool()
   def logarithm(n: float, base: float = 10) -> float:
       \"\"\"Calculate logarithm.\"\"\"
       import math
       if n <= 0 or base <= 0:
           return float('nan')
       return math.log(n, base)
   
   The server automatically:
   - Generates the MCP schema
   - Handles parameter validation
   - Returns results
   - Provides error handling


6. DEPLOYMENT
   ─────────────────────────────────────────────────────────────────────────
   
   Production deployment:
   
   # Run in a dedicated process
   python mcp_calculator_server.py
   
   # Or with process manager (systemd, supervisor, etc.)
   
   # Or in a container
   Dockerfile:
   FROM python:3.11
   WORKDIR /app
   COPY mcp_calculator_server.py .
   COPY Pipfile .
   RUN pipenv install --system
   CMD ["python", "mcp_calculator_server.py"]
   
   # Or as a module import
   from mcp_calculator_server import mcp
   mcp.run(transport="stdio")


7. TROUBLESHOOTING
   ─────────────────────────────────────────────────────────────────────────
   
   Server won't start:
   - Check Python version: python --version (needs 3.10+)
   - Check dependencies: pipenv install
   - Run with: python -u mcp_calculator_server.py
   
   Connection refused:
   - Make sure server is running in another terminal
   - Check stdio transport is being used
   
   Tool not found:
   - Server must be running
   - Tool names are case-sensitive
   - Check function is decorated with @mcp.tool()


8. RESOURCES
   ─────────────────────────────────────────────────────────────────────────
   
   - MCP Specification: https://spec.modelcontextprotocol.io
   - Python SDK: https://github.com/modelcontextprotocol/python-sdk
   - FastMCP Docs: https://pdme.ai/docs/libraries/python/usage


═══════════════════════════════════════════════════════════════════════════

QUICK START:

  Terminal 1: python mcp_calculator_server.py
  
  Terminal 2: (use Claude, LangChain, or custom client)
  
  See MCP_SETUP.md for detailed documentation.

═══════════════════════════════════════════════════════════════════════════
""")
