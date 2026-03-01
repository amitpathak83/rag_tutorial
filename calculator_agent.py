#!/usr/bin/env python3
"""
Calculator Agentic Flow using Ollama
An AI agent that processes natural language math queries and performs calculations.
"""

import json
from typing import Any
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from langgraph.graph import StateGraph, END, MessagesState


# ============================================================================
# CALCULATOR TOOLS - Define individual math operations
# ============================================================================

@tool
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    print(f"Adding {a} and {b}")
    return a + b


@tool
def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    print(f"Subtracting {b} from {a}")
    return a - b


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    print(f"Multiplying {a} and {b}")
    return a * b


@tool
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    print(f"Dividing {a} by {b}")
    if b == 0:
        return float('inf')
    return a / b


@tool
def power(base: float, exponent: float) -> float:
    """Raise base to the power of exponent."""
    print(f"Raising {base} to the power of {exponent}")
    return base ** exponent


@tool
def square_root(n: float) -> float:
    """Calculate the square root of a number."""
    print(f"Calculating the square root of {n}")
    if n < 0:
        return float('nan')
    return n ** 0.5


@tool
def percentage(value: float, percent: float) -> float:
    """Calculate a percentage of a value."""
    print(f"Calculating {percent}% of {value}")
    return (value * percent) / 100


tools = [add, subtract, multiply, divide, power, square_root, percentage]


# ============================================================================
# AGENT STATE AND LOGIC
# ============================================================================

def create_calculator_agent():
    """Create and return a calculator agent using LangGraph."""

    # Initialize the Ollama LLM
    # Make sure Ollama is running: ollama serve
    # You can use different models like 'mistral', 'neural-chat', 'dolphin-mixtral', etc.
    llm = ChatOllama(
        model="llama3.2",  # Change this to your preferred Ollama model
        temperature=0.7,
        base_url="http://localhost:11434",
    )

    # Bind tools to the LLM
    llm_with_tools = llm.bind_tools(tools)

    # ========================
    # Define Graph Nodes
    # ========================

    def agent_node(state: MessagesState):
        """The main agent node that decides what to do."""
        messages = state["messages"]
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    def tools_node(state: MessagesState):
        """Execute the tools that the agent requests."""
        messages = state["messages"]
        last_message = messages[-1]

        tool_results = []

        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            for tool_call in last_message.tool_calls:
                tool_name = tool_call["name"]
                tool_input = tool_call["args"]

                # Map tool names to functions
                tool_map = {
                    "add": add.invoke,
                    "subtract": subtract.invoke,
                    "multiply": multiply.invoke,
                    "divide": divide.invoke,
                    "power": power.invoke,
                    "square_root": square_root.invoke,
                    "percentage": percentage.invoke,
                }

                if tool_name in tool_map:
                    result = tool_map[tool_name](tool_input)
                    tool_results.append(
                        ToolMessage(
                            content=str(result),
                            tool_call_id=tool_call["id"],
                            name=tool_name,
                        )
                    )

        return {"messages": tool_results}

    # ========================
    # Define Edge Logic
    # ========================

    def should_continue(state: MessagesState):
        """Determine whether to continue or end."""
        messages = state["messages"]
        last_message = messages[-1]

        # If the LLM didn't call any tools, end
        if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
            return "end"

        return "continue"

    # ========================
    # Build the Graph
    # ========================

    workflow = StateGraph(MessagesState)

    # Add nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tools_node)

    # Set entry point
    workflow.set_entry_point("agent")

    # Add conditional edge
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END,
        }
    )

    # Tools always go back to agent
    workflow.add_edge("tools", "agent")

    # Compile the graph
    return workflow.compile()


# ============================================================================
# MAIN INTERACTION FUNCTION
# ============================================================================

def run_calculator_agent(query: str):
    """Run the calculator agent with a user query."""
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print(f"{'='*60}\n")

    agent = create_calculator_agent()

    # Create initial message
    messages = [HumanMessage(content=query)]

    # Run the agent
    try:
        result = agent.invoke({"messages": messages})

        # Extract the final response
        final_message = result["messages"][-1]
        print(f"Result: {final_message.content}\n")

        return final_message.content

    except Exception as e:
        print(f"Error: {e}\n")
        return None


# ============================================================================
# EXAMPLE QUERIES
# ============================================================================

if __name__ == "__main__":
    # Example queries
    queries = [
        "how may eggs in ten dozens?",
        "Calculate 100 minus 35",
        "Multiply 12 by 8",
        "What is 144 divided by 12?",
        "What is 2 to the power of 10?",
        "What is the square root of 144?",
        "Calculate 20% of 500",
        "Add 15, 25, and 10 together",
        "What is 99 divided by 3 plus 5?",
    ]

    print("\n" + "="*60)
    print("CALCULATOR AGENTIC FLOW - POWERED BY OLLAMA")
    print("="*60)
    print("\nMake sure Ollama is running:")
    print("  $ ollama serve")
    print("\nYou can use any Ollama model. Common options:")
    print("  - mistral (recommended for speed)")
    print("  - neural-chat")
    print("  - dolphin-mixtral")
    print("  - llama2")

    # Run a subset of queries
    for query in queries[:5]:  # Run first 3 examples
        try:
            run_calculator_agent(query)
        except Exception as e:
            print(f"Error processing '{query}': {e}\n")
