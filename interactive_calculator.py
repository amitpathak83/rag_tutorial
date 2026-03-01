#!/usr/bin/env python3
"""
Interactive Calculator Agentic Flow
A user-friendly interface for the calculator agent.
"""

import sys
from calculator_agent import run_calculator_agent


def print_header():
    """Print the application header."""
    print("\n" + "="*70)
    print("  CALCULATOR AGENTIC FLOW - INTERACTIVE MODE")
    print("="*70)
    print("\nPowered by Ollama + LangChain + LangGraph")
    print("\nUsage: Ask math questions in natural language")
    print("Examples:")
    print("  - What is 25 plus 17?")
    print("  - Multiply 12 by 8")
    print("  - What is 2 to the power of 10?")
    print("  - Calculate 20% of 500")
    print("\nCommands:")
    print("  - 'help'     : Show this help message")
    print("  - 'examples' : Show more examples")
    print("  - 'quit'     : Exit the program")
    print("="*70)


def print_examples():
    """Print example queries."""
    examples = [
        "What is 25 plus 17?",
        "Calculate 100 minus 35",
        "Multiply 12 by 8",
        "What is 144 divided by 12?",
        "What is 2 to the power of 10?",
        "What is the square root of 144?",
        "Calculate 20% of 500",
        "Add 15, 25, and 10 together",
        "What is 99 divided by 3 plus 5?",
        "What is the square root of 256?",
        "Subtract 42 from 100",
        "What is 7 times 8?",
    ]

    print("\nExample Queries:")
    print("-" * 50)
    for i, example in enumerate(examples, 1):
        print(f"{i:2d}. {example}")
    print("-" * 50)


def main():
    """Main interactive loop."""
    print_header()

    print("\nNote: Make sure Ollama is running!")
    print("  $ ollama serve")
    print("  $ ollama pull mistral  # (if not already pulled)")

    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()

            # Handle empty input
            if not user_input:
                continue

            # Handle commands
            if user_input.lower() == "quit":
                print("\nExiting... Goodbye!")
                break
            elif user_input.lower() == "help":
                print_header()
            elif user_input.lower() == "examples":
                print_examples()
            else:
                # Run the calculator agent
                run_calculator_agent(user_input)

        except KeyboardInterrupt:
            print("\n\nExiting... Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please make sure Ollama is running and the model is downloaded.")


if __name__ == "__main__":
    main()
