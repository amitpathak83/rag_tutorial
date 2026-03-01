#!/usr/bin/env python3
"""
MCP Calculator Integration
Shows how to integrate the MCP Calculator Server with LLM agents.
Demonstrates using MCP tools in an agentic workflow.
"""

import asyncio
import json
from typing import Any

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from langgraph.graph import StateGraph, END, MessagesState

from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


# ============================================================================
# MCP CLIENT WRAPPER
# ============================================================================

class MCPCalculatorWrapper:
    """Wrapper to use MCP Calculator Server tools in agents."""

    def __init__(self):
        """Initialize the MCP wrapper."""
        self.transport = None
        self.session = None

    async def initialize(self):
        """Initialize connection to MCP server."""
        self.transport = StdioClientTransport(
            "python mcp_calculator_server.py")
        self.session = ClientSession(self.transport)

        # Start the transport
        await self.transport.__aenter__()
        await self.session.__aenter__()

        # Initialize the session
        await self.session.initialize()

    async def call_tool(self, tool_name: str, **kwargs) -> str:
        """Call a tool on the MCP server."""
        if not self.session:
            raise RuntimeError("MCP client not initialized")

        result = await self.session.call_tool(tool_name, kwargs)
        if result.content:
            return result.content[0].text
        return "No result"

    async def cleanup(self):
        """Clean up connections."""
        if self.session:
            await self.session.__aexit__(None, None, None)
        if self.transport:
            await self.transport.__aexit__(None, None, None)


# ============================================================================
# AGENT WITH MCP TOOLS
# ============================================================================

class MCPCalculatorAgent:
    """Agent that uses MCP Calculator Server for calculations."""

    def __init__(self):
        """Initialize the agent."""
        self.mcp_client = MCPCalculatorWrapper()
        self.llm = ChatOllama(
            model="mistral",
            temperature=0.3,
            base_url="http://localhost:11434",
        )

        # Define MCP tool functions for the agent
        @tool
        async def add(a: float, b: float) -> float:
            """Add two numbers via MCP."""
            result = await self.mcp_client.call_tool("add", a=a, b=b)
            return float(result)

        @tool
        async def subtract(a: float, b: float) -> float:
            """Subtract via MCP."""
            result = await self.mcp_client.call_tool("subtract", a=a, b=b)
            return float(result)

        @tool
        async def multiply(a: float, b: float) -> float:
            """Multiply via MCP."""
            result = await self.mcp_client.call_tool("multiply", a=a, b=b)
            return float(result)

        @tool
        async def divide(a: float, b: float) -> float:
            """Divide via MCP."""
            result = await self.mcp_client.call_tool("divide", a=a, b=b)
            return float(result)

        @tool
        async def power(base: float, exponent: float) -> float:
            """Power via MCP."""
            result = await self.mcp_client.call_tool("power", base=base, exponent=exponent)
            return float(result)

        @tool
        async def square_root(n: float) -> float:
            """Square root via MCP."""
            result = await self.mcp_client.call_tool("square_root", n=n)
            return float(result)

        @tool
        async def percentage(value: float, percent: float) -> float:
            """Percentage via MCP."""
            result = await self.mcp_client.call_tool("percentage", value=value, percent=percent)
            return float(result)

        self.tools = [add, subtract, multiply,
                      divide, power, square_root, percentage]
        self.llm_with_tools = self.llm.bind_tools(self.tools)

    async def initialize(self):
        """Initialize the agent and MCP connection."""
        await self.mcp_client.initialize()

    async def process_query(self, query: str) -> str:
        """Process a math query."""
        print(f"\n{'='*70}")
        print(f"Query: {query}")
        print(f"{'='*70}\n")

        messages = [HumanMessage(content=query)]

        # Simple agentic loop
        max_iterations = 10
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            # Get LLM response
            response = self.llm_with_tools.invoke(messages)
            messages.append(response)

            # Check if we should continue
            if not hasattr(response, "tool_calls") or not response.tool_calls:
                # No more tools to call, return final response
                print(f"\nAnswer: {response.content}\n")
                return response.content

            # Execute tools
            tool_results = []
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                print(
                    f"Calling tool: {tool_name}({', '.join(f'{k}={v}' for k, v in tool_args.items())})")

                # Call the tool
                for tool in self.tools:
                    if tool.name == tool_name:
                        try:
                            result = await tool.invoke(tool_args)
                            print(f"  Result: {result}")
                            tool_results.append(
                                ToolMessage(
                                    content=str(result),
                                    tool_call_id=tool_call["id"],
                                    name=tool_name,
                                )
                            )
                        except Exception as e:
                            print(f"  Error: {e}")
                            tool_results.append(
                                ToolMessage(
                                    content=f"Error: {str(e)}",
                                    tool_call_id=tool_call["id"],
                                    name=tool_name,
                                    is_error=True,
                                )
                            )
                        break

            # Add tool results to messages
            messages.extend(tool_results)

        return "Max iterations reached"

    async def cleanup(self):
        """Clean up resources."""
        await self.mcp_client.cleanup()


# ============================================================================
# MAIN
# ============================================================================

async def main():
    """Main entry point."""
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║          MCP CALCULATOR INTEGRATION - AGENT EXAMPLE                      ║
╚══════════════════════════════════════════════════════════════════════════╝

This example shows how to integrate the MCP Calculator Server with
an LLM agent using LangGraph.

Prerequisites:
  1. Start the MCP server: python mcp_calculator_server.py
  2. Start Ollama: ollama serve
  3. Install model: ollama pull mistral

═══════════════════════════════════════════════════════════════════════════
    """)

    # Create and initialize agent
    agent = MCPCalculatorAgent()

    try:
        print("Initializing agent and connecting to MCP server...")
        await agent.initialize()
        print("✓ Agent initialized\n")

        # Example queries
        queries = [
            "What is 25 plus 17?",
            "Multiply 12 by 8",
            "What is 2 to the power of 10?",
            "Calculate 20% of 500",
        ]

        for query in queries:
            try:
                await agent.process_query(query)
            except Exception as e:
                print(f"Error: {e}\n")

    finally:
        print("Cleaning up...")
        await agent.cleanup()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Interactive mode
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║          MCP CALCULATOR INTEGRATION - INTERACTIVE MODE                   ║
╚══════════════════════════════════════════════════════════════════════════╝

Ask any math question and the agent will solve it using the MCP server.

Examples:
  - What is 25 plus 17?
  - Multiply 12 by 8
  - What is 2 to the power of 10?
  - Calculate 20% of 500

═══════════════════════════════════════════════════════════════════════════
        """)

        agent = MCPCalculatorAgent()

        async def interactive():
            await agent.initialize()

            while True:
                try:
                    query = input("\nYou: ").strip()
                    if not query:
                        continue
                    if query.lower() == "quit":
                        break

                    await agent.process_query(query)

                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"Error: {e}")

            await agent.cleanup()

        asyncio.run(interactive())
    else:
        asyncio.run(main())
