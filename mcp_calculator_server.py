#!/usr/bin/env python3
"""
MCP Calculator Server
A Model Context Protocol server that exposes calculator tools for remote access.
Uses FastMCP for simplified implementation.
"""

import sys
from mcp.server.fastmcp import FastMCP

# ============================================================================
# CALCULATOR TOOLS - Define individual math operations
# ============================================================================


class CalculatorTools:
    """Container for all calculator operations."""

    @staticmethod
    def add(a: float, b: float) -> float:
        """Add two numbers together."""
        return a + b

    @staticmethod
    def subtract(a: float, b: float) -> float:
        """Subtract b from a."""
        return a - b

    @staticmethod
    def multiply(a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b

    @staticmethod
    def divide(a: float, b: float) -> float:
        """Divide a by b."""
        if b == 0:
            return float('inf')
        return a / b

    @staticmethod
    def power(base: float, exponent: float) -> float:
        """Raise base to the power of exponent."""
        print(f"Raising {base} to the power of {exponent}")
        return base ** exponent

    @staticmethod
    def square_root(n: float) -> float:
        """Calculate the square root of a number."""
        if n < 0:
            return float('nan')
        return n ** 0.5

    @staticmethod
    def percentage(value: float, percent: float) -> float:
        """Calculate a percentage of a value."""
        print(f"Calculating {percent}% of {value}")
        return (value * percent) / 100

    @staticmethod
    def modulo(a: float, b: float) -> float:
        """Get the remainder of a divided by b."""
        print(f"Calculating {a} modulo {b}")
        if b == 0:
            return float('nan')
        return a % b

    @staticmethod
    def average(numbers: list) -> float:
        """Calculate the average of multiple numbers."""
        if not numbers:
            return 0
        return sum(numbers) / len(numbers)

    @staticmethod
    def factorial(n: int) -> int:
        """Calculate the factorial of a number."""
        print(f"Calculating factorial of {n}")
        if n < 0:
            return -1
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result


# ============================================================================
# FASTMCP SERVER
# ============================================================================

# Initialize FastMCP server
mcp = FastMCP("calculator-server")
tools = CalculatorTools()


# Define tools
@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    print(f"Adding {a} and {b}")
    return tools.add(a, b)


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    print(f"Subtracting {b} from {a}")
    return tools.subtract(a, b)


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    print(f"Multiplying {a} and {b}")
    return tools.multiply(a, b)


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    return tools.divide(a, b)


@mcp.tool()
def power(base: float, exponent: float) -> float:
    """Raise base to the power of exponent."""
    return tools.power(base, exponent)


@mcp.tool()
def square_root(n: float) -> float:
    """Calculate the square root of a number."""
    return tools.square_root(n)


@mcp.tool()
def percentage(value: float, percent: float) -> float:
    """Calculate a percentage of a value."""
    return tools.percentage(value, percent)


@mcp.tool()
def modulo(a: float, b: float) -> float:
    """Get the remainder of a divided by b."""
    return tools.modulo(a, b)


@mcp.tool()
def average(numbers: list) -> float:
    """Calculate the average of multiple numbers."""
    return tools.average(numbers)


@mcp.tool()
def factorial(n: int) -> int:
    """Calculate the factorial of a number."""
    return tools.factorial(n)


# ============================================================================
# MAIN
# ============================================================================


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║               MCP CALCULATOR SERVER - Starting                           ║
╚══════════════════════════════════════════════════════════════════════════╝

Available Tools:
  • add              - Add two numbers
  • subtract         - Subtract two numbers
  • multiply         - Multiply two numbers
  • divide           - Divide two numbers
  • power            - Raise base to exponent
  • square_root      - Calculate square root
  • percentage       - Calculate percentage
  • modulo           - Get remainder
  • average          - Calculate average
  • factorial        - Calculate factorial

═══════════════════════════════════════════════════════════════════════════
    """, file=sys.stderr)

    mcp.run(transport="stdio")
