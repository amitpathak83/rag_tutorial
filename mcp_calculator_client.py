#!/usr/bin/env python3
"""
MCP Calculator Client
A client that connects to the MCP Calculator Server and uses its tools.
"""

import asyncio
import json
from typing import Optional, Any
import sys
import subprocess

from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.types import Tool


class CalculatorMCPClient:
    """Client for interacting with the Calculator MCP Server."""

    def __init__(self):
        """Initialize the client."""
        self.session: Optional[ClientSession] = None
        self.transport = None

    async def connect(self, server_command: str = "python mcp_calculator_server.py"):
        """
        Connect to the MCP server.

        Args:
            server_command: Command to start the server
        """
        print(f"Connecting to MCP Server: {server_command}")

        # Parse the command
        parts = server_command.split()

        # Create stdio transport to communicate with server
        self.transport = stdio_client(
            StdioServerParameters(
                command=parts[0],
                args=parts[1:]
            )
        )

        # Create session from transport
        self.session = ClientSession(self.transport)
        async with self.transport as t:
            async with ClientSession(t) as session:
                await session.initialize()
                # Get available tools
                tools_response = await session.list_tools()
                print(f"✓ Available tools: {len(tools_response.tools)}")

        return self.session

    async def call_tool(self, tool_name: str, **arguments) -> str:
        """
        Call a tool on the server.

        Args:
            tool_name: Name of the tool to call
            **arguments: Tool arguments

        Returns:
            Tool result as string
        """
        if not self.session:
            raise RuntimeError("Not connected to server")

        try:
            result = await self.session.call_tool(tool_name, arguments)

            if result.content:
                return result.content[0].text
            return "No result"

        except Exception as e:
            return f"Error calling {tool_name}: {str(e)}"

    async def list_tools(self) -> list[dict]:
        """Get list of available tools."""
        if not self.session:
            raise RuntimeError("Not connected to server")

        tools_response = await self.session.list_tools()
        tools = []

        for tool in tools_response.tools:
            tools.append({
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            })

        return tools


# ============================================================================
# INTERACTIVE CLIENT
# ============================================================================

async def interactive_client():
    """Run the client in interactive mode."""
    client = CalculatorMCPClient()

    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║               MCP CALCULATOR CLIENT - Interactive Mode                   ║
╚══════════════════════════════════════════════════════════════════════════╝

Available Commands:
  list              - List available tools
  <tool> <args>     - Call a tool (e.g., "add 5 3")
  help              - Show this help message
  quit              - Exit the client

Tool Examples:
  add 5 3
  multiply 12 8
  power 2 10
  square_root 144
  percentage 500 20
  factorial 5
  average 10 20 30 40 50

═══════════════════════════════════════════════════════════════════════════
    """)

    try:
        async with stdio_client(
            StdioServerParameters(
                command="python3",
                args=["mcp_calculator_server.py"]
            )
        ) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                print("✓ Connected to MCP Server\n")

                # Interactive loop
                while True:
                    try:
                        loop = asyncio.get_event_loop()
                        command = await loop.run_in_executor(None, input, "You: ")
                        command = command.strip()

                        if not command:
                            continue

                        if command.lower() == "quit":
                            print("Exiting...")
                            break

                        elif command.lower() == "help":
                            print("""
Available Tools:
  add, subtract, multiply, divide, power, square_root,
  percentage, modulo, average, factorial

Examples:
  add 5 3              → Returns 8
  multiply 12 8        → Returns 96
  power 2 10           → Returns 1024
  square_root 144      → Returns 12.0
  percentage 500 20    → Returns 100.0
  factorial 5          → Returns 120
  average 10 20 30     → Returns 20.0
                            """)

                        elif command.lower() == "list":
                            tools_response = await session.list_tools()
                            print("\nAvailable Tools:")
                            print("-" * 50)
                            for tool in tools_response.tools:
                                print(f"\n  {tool.name}")
                                print(f"    {tool.description}")
                            print("-" * 50 + "\n")

                        else:
                            # Parse command as tool call
                            parts = command.split()
                            if len(parts) < 1:
                                continue

                            tool_name = parts[0]
                            args = parts[1:]

                            # Convert arguments to appropriate types
                            try:
                                # Try to convert to numbers
                                converted_args = []
                                for arg in args:
                                    try:
                                        if "." in arg:
                                            converted_args.append(float(arg))
                                        else:
                                            converted_args.append(int(arg))
                                    except ValueError:
                                        converted_args.append(arg)

                                # Build arguments dict based on tool
                                arguments = {}
                                if tool_name in ["add", "subtract", "multiply", "divide", "power", "modulo"]:
                                    if len(converted_args) >= 2:
                                        arguments = {
                                            "a": converted_args[0], "b": converted_args[1]}
                                elif tool_name in ["square_root"]:
                                    if len(converted_args) >= 1:
                                        arguments = {"n": converted_args[0]}
                                elif tool_name == "percentage":
                                    if len(converted_args) >= 2:
                                        arguments = {
                                            "value": converted_args[0], "percent": converted_args[1]}
                                elif tool_name == "average":
                                    arguments = {"numbers": converted_args}
                                elif tool_name == "factorial":
                                    if len(converted_args) >= 1:
                                        arguments = {
                                            "n": int(converted_args[0])}

                                if arguments:
                                    result = await session.call_tool(tool_name, arguments)
                                    if result.content:
                                        print(
                                            f"Result: {result.content[0].text}\n")
                                else:
                                    print(
                                        f"Invalid arguments for {tool_name}\n")

                            except Exception as e:
                                print(f"Error: {str(e)}\n")

                    except KeyboardInterrupt:
                        print("\n\nExiting...")
                        break
                    except Exception as e:
                        print(f"Error: {str(e)}\n")
    except Exception as e:
        print(f"Connection error: {e}")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

async def demo_client():
    """Run the client with example calculations."""

    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║               MCP CALCULATOR CLIENT - Demo Mode                          ║
╚══════════════════════════════════════════════════════════════════════════╝

Running calculations via MCP Server...

    """)

    try:
        async with stdio_client(
            StdioServerParameters(
                command="python3",
                args=["mcp_calculator_server.py"]
            )
        ) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                print("✓ Connected to MCP Server\n")

                # Example calculations
                examples = [
                    ("add", {"a": 25, "b": 17}, "25 + 17"),
                    ("multiply", {"a": 12, "b": 8}, "12 × 8"),
                    ("divide", {"a": 144, "b": 12}, "144 ÷ 12"),
                    ("power", {"base": 2, "exponent": 10}, "2^10"),
                    ("square_root", {"n": 144}, "√144"),
                    ("percentage", {"value": 500,
                     "percent": 20}, "20% of 500"),
                    ("factorial", {"n": 5}, "5!"),
                    ("average", {"numbers": [10, 20, 30, 40, 50]},
                     "average(10, 20, 30, 40, 50)"),
                ]

                for tool_name, arguments, display in examples:
                    try:
                        result = await session.call_tool(tool_name, arguments)
                        if result.content:
                            print(f"  {display:30} = {result.content[0].text}")
                    except Exception as e:
                        print(f"  {display:30} = Error: {e}")

                print("\n" + "="*70 + "\n")
    except Exception as e:
        print(f"Error: {e}")


# ============================================================================
# MAIN
# ============================================================================

async def main():
    """Main entry point."""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        await demo_client()
    else:
        await interactive_client()


if __name__ == "__main__":
    import os
    import io

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except BaseException as e:
        # Suppress TaskGroup exceptions from MCP library
        error_name = type(e).__name__
        if error_name not in ("ExceptionGroup",) and "TaskGroup" not in error_name:
            print(f"Error: {e}")
