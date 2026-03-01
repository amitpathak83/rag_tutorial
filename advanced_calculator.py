#!/usr/bin/env python3
"""
Advanced Calculator Agent
Demonstrates advanced agentic patterns and extensions.
"""

import json
from typing import Any, Annotated
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from langgraph.graph import StateGraph, END, MessagesState
from langgraph.prebuilt import ToolNode


# ============================================================================
# EXTENDED CALCULATOR TOOLS
# ============================================================================

@tool
def add(*numbers: float) -> float:
    """Add multiple numbers together."""
    return sum(numbers)


@tool
def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b


@tool
def multiply(*numbers: float) -> float:
    """Multiply multiple numbers together."""
    result = 1
    for n in numbers:
        result *= n
    return result


@tool
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        return float('inf')
    return a / b


@tool
def power(base: float, exponent: float) -> float:
    """Raise base to the power of exponent."""
    return base ** exponent


@tool
def square_root(n: float) -> float:
    """Calculate the square root of a number."""
    if n < 0:
        return float('nan')
    return n ** 0.5


@tool
def absolute_value(n: float) -> float:
    """Get the absolute value of a number."""
    return abs(n)


@tool
def modulo(a: float, b: float) -> float:
    """Get the remainder of a divided by b."""
    if b == 0:
        return float('nan')
    return a % b


@tool
def average(*numbers: float) -> float:
    """Calculate the average of multiple numbers."""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)


@tool
def factorial(n: int) -> int:
    """Calculate the factorial of a number."""
    if n < 0:
        return -1
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


@tool
def percentage(value: float, percent: float) -> float:
    """Calculate a percentage of a value."""
    return (value * percent) / 100


@tool
def percentage_of(part: float, whole: float) -> float:
    """Calculate what percentage part is of whole."""
    if whole == 0:
        return float('nan')
    return (part / whole) * 100


@tool
def compound_interest(principal: float, rate: float, time: float, compound_periods: int = 1) -> float:
    """Calculate compound interest: A = P(1 + r/n)^(nt)"""
    if rate < 0:
        return -1
    return principal * ((1 + rate / (100 * compound_periods)) ** (compound_periods * time))


tools = [
    add, subtract, multiply, divide, power, square_root, absolute_value,
    modulo, average, factorial, percentage, percentage_of, compound_interest
]


# ============================================================================
# ADVANCED AGENT WITH STREAMING SUPPORT
# ============================================================================

class AdvancedCalculatorAgent:
    """Advanced calculator agent with extended features."""

    def __init__(self, model: str = "mistral", temperature: float = 0.3):
        """Initialize the advanced calculator agent."""
        self.model = model
        self.temperature = temperature
        self.llm = ChatOllama(
            model=model,
            temperature=temperature,
            base_url="http://localhost:11434",
        )
        self.llm_with_tools = self.llm.bind_tools(tools)
        self.graph = self._build_graph()

    def _build_graph(self):
        """Build the computational graph."""

        def agent_node(state: MessagesState):
            """Agent decision node."""
            messages = state["messages"]
            response = self.llm_with_tools.invoke(messages)
            return {"messages": [response]}

        def router(state: MessagesState):
            """Route to tools or end."""
            messages = state["messages"]
            last_message = messages[-1]

            if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                return "tools"
            return "end"

        workflow = StateGraph(MessagesState)
        workflow.add_node("agent", agent_node)
        workflow.add_node("tools", ToolNode(tools))

        workflow.set_entry_point("agent")
        workflow.add_conditional_edges(
            "agent", router, {"tools": "tools", "end": END})
        workflow.add_edge("tools", "agent")

        return workflow.compile()

    def ask(self, query: str, show_steps: bool = False):
        """
        Ask the calculator agent a question.

        Args:
            query: The math question in natural language
            show_steps: Whether to show intermediate steps

        Returns:
            The final answer
        """
        if show_steps:
            print(f"\n{'='*60}")
            print(f"Query: {query}")
            print(f"{'='*60}\n")

        messages = [HumanMessage(content=query)]

        try:
            result = self.graph.invoke({"messages": messages})
            final_message = result["messages"][-1]

            if show_steps:
                print(f"Answer: {final_message.content}\n")

            return final_message.content

        except Exception as e:
            return f"Error: {str(e)}"


# ============================================================================
# DEMO FUNCTIONS
# ============================================================================

def demo_basic_calculations():
    """Demonstrate basic calculations."""
    print("\n" + "="*70)
    print("DEMO 1: Basic Calculations")
    print("="*70)

    agent = AdvancedCalculatorAgent()

    queries = [
        "What is 25 plus 17?",
        "Multiply 12 by 8",
        "What is 144 divided by 12?",
    ]

    for query in queries:
        agent.ask(query, show_steps=True)


def demo_advanced_calculations():
    """Demonstrate advanced calculations."""
    print("\n" + "="*70)
    print("DEMO 2: Advanced Calculations")
    print("="*70)

    agent = AdvancedCalculatorAgent()

    queries = [
        "What is 2 to the power of 10?",
        "Calculate the average of 10, 20, 30, 40, and 50",
        "What is 15% of 300?",
        "What percentage is 25 out of 200?",
    ]

    for query in queries:
        agent.ask(query, show_steps=True)


def demo_financial_calculations():
    """Demonstrate financial calculations."""
    print("\n" + "="*70)
    print("DEMO 3: Financial Calculations")
    print("="*70)

    agent = AdvancedCalculatorAgent()

    queries = [
        "If I invest $1000 at 5% interest compounded annually for 2 years, how much will I have?",
        "Calculate 10% of a $5000 investment",
    ]

    for query in queries:
        agent.ask(query, show_steps=True)


def demo_custom_model():
    """Demonstrate using a different Ollama model."""
    print("\n" + "="*70)
    print("DEMO 4: Using Custom Model")
    print("="*70)

    # Try with neural-chat model (more optimized for conversation)
    agent = AdvancedCalculatorAgent(model="neural-chat", temperature=0.5)

    query = "What is the factorial of 5?"
    agent.ask(query, show_steps=True)


# ============================================================================
# INTERACTIVE MODE
# ============================================================================

def interactive_mode():
    """Run the agent in interactive mode."""
    print("\n" + "="*70)
    print("ADVANCED CALCULATOR AGENT - INTERACTIVE MODE")
    print("="*70)
    print("\nAvailable tools:")
    print("  • Basic: add, subtract, multiply, divide")
    print("  • Advanced: power, square_root, factorial, modulo")
    print("  • Financial: compound_interest, percentage")
    print("  • Statistical: average, percentage_of")
    print("\nCommands: 'demo', 'quit', or ask any math question")
    print("="*70)

    agent = AdvancedCalculatorAgent()

    while True:
        try:
            query = input("\nYou: ").strip()

            if not query:
                continue
            elif query.lower() == "quit":
                print("\nExiting...")
                break
            elif query.lower() == "demo":
                # Run a quick demo
                demo_advanced_calculations()
            else:
                agent.ask(query, show_steps=True)

        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import sys

    print("\nAdvanced Calculator Agent - Demo & Interactive Mode")
    print("Make sure Ollama is running: ollama serve")

    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "demo1":
            demo_basic_calculations()
        elif command == "demo2":
            demo_advanced_calculations()
        elif command == "demo3":
            demo_financial_calculations()
        elif command == "demo4":
            demo_custom_model()
        elif command == "all":
            demo_basic_calculations()
            demo_advanced_calculations()
            demo_financial_calculations()
        else:
            print(f"Unknown command: {command}")
    else:
        interactive_mode()
