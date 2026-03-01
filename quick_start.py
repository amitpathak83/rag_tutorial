#!/usr/bin/env python3
"""
Quick Start Guide for Calculator Agentic Flow
"""

QUICK_START = """
╔══════════════════════════════════════════════════════════════════════════╗
║                  CALCULATOR AGENTIC FLOW - QUICK START                   ║
╚══════════════════════════════════════════════════════════════════════════╝

📋 PROJECT STRUCTURE:
  calculator_agent.py          - Core calculator agent implementation
  advanced_calculator.py       - Extended agent with more tools
  interactive_calculator.py    - Interactive user interface
  README.md                    - Full documentation
  quick_start.py              - This file

⚡ SETUP (One-time):
  
  1. Install Ollama:
     - macOS: brew install ollama
     - Or download from https://ollama.ai
  
  2. Start Ollama server (keep running in background):
     $ ollama serve
  
  3. Download a model (in another terminal):
     $ ollama pull mistral
     (or: neural-chat, dolphin-mixtral, llama2)
  
  4. Install Python dependencies:
     $ pipenv install
     $ pipenv shell

🚀 QUICK COMMANDS:

  Basic Calculator (Examples):
    $ python calculator_agent.py
  
  Interactive Mode (Chat with calculator):
    $ python interactive_calculator.py
  
  Advanced Features:
    $ python advanced_calculator.py              # Interactive mode
    $ python advanced_calculator.py demo1        # Demo: Basic math
    $ python advanced_calculator.py demo2        # Demo: Advanced math
    $ python advanced_calculator.py demo3        # Demo: Financial
    $ python advanced_calculator.py all          # Run all demos

💬 EXAMPLE QUESTIONS:

  Basic:
    "What is 25 plus 17?"
    "Multiply 12 by 8"
    "What is 144 divided by 12?"
  
  Advanced:
    "What is 2 to the power of 10?"
    "Calculate the square root of 256"
    "What is the factorial of 5?"
  
  Financial:
    "If I invest $1000 at 5% interest for 2 years, how much will I have?"
    "What percentage is 25 out of 200?"
  
  Multi-step:
    "Add 10, 20, and 30 together, then divide by 3"
    "What is 10% of 500?"

🔧 HOW IT WORKS:

  1. User asks a question in natural language
  2. Ollama LLM analyzes the query
  3. LLM decides which calculator tools to call
  4. Tools execute the calculations
  5. Results are returned to the LLM
  6. LLM provides the final answer

🛠️ CUSTOMIZATION:

  Change Model (edit calculator_agent.py line ~68):
    model="mistral"          # Default (fast)
    model="neural-chat"      # Good for conversation
    model="dolphin-mixtral"  # Powerful but slower
    model="llama2"          # General purpose

  Add More Tools (advanced_calculator.py):
    @tool
    def logarithm(n: float, base: float = 10) -> float:
        \"\"\"Calculate logarithm.\"\"\"
        import math
        return math.log(n, base)
    
    # Add to tools list:
    tools = [..., logarithm]

📚 ARCHITECTURE:

  ┌─ User Input (Natural Language)
  │
  ├─ Ollama LLM (Agent Layer)
  │  └─ Understands intent
  │  └─ Plans tool usage
  │
  ├─ Tool Selection Layer
  │  └─ Maps tools to function calls
  │
  ├─ Execution Layer
  │  └─ Runs calculations
  │
  └─ Response Generation
     └─ Final answer to user

🐛 TROUBLESHOOTING:

  Error: "Connection refused"
    → Make sure Ollama is running: ollama serve
  
  Error: "Model not found"
    → Download the model: ollama pull mistral
  
  Error: "Slow response"
    → Try a smaller model like 'mistral' or 'neural-chat'
  
  Error: "Wrong answer"
    → Try different temperature (0.3-0.7) or a different model

✨ KEY FEATURES:

  ✓ Natural language understanding
  ✓ Multi-step calculations
  ✓ Automatic tool selection
  ✓ Error handling
  ✓ Financial calculations
  ✓ Statistical operations
  ✓ Extensible tool system
  ✓ Interactive mode
  ✓ Demo examples

📖 USEFUL LINKS:

  Ollama: https://ollama.ai
  LangChain: https://python.langchain.com
  LangGraph: https://langchain-ai.github.io/langgraph
  MCP: https://modelcontextprotocol.io

🎯 NEXT STEPS:

  1. Run: python calculator_agent.py
  2. Try: python interactive_calculator.py
  3. Explore: python advanced_calculator.py demo2
  4. Customize: Add your own tools!

═══════════════════════════════════════════════════════════════════════════
"""


def main():
    """Print the quick start guide."""
    print(QUICK_START)


if __name__ == "__main__":
    main()

# Additional reference chart
TOOL_REFERENCE = {
    "Basic Operations": {
        "add": "Add multiple numbers",
        "subtract": "Subtract b from a",
        "multiply": "Multiply numbers",
        "divide": "Divide a by b",
    },
    "Advanced Math": {
        "power": "Raise base to exponent",
        "square_root": "Calculate square root",
        "absolute_value": "Get absolute value",
        "modulo": "Get remainder",
        "factorial": "Calculate factorial",
    },
    "Statistical": {
        "average": "Calculate average of numbers",
        "percentage": "Calculate percentage of value",
        "percentage_of": "Calculate what % part is of whole",
    },
    "Financial": {
        "compound_interest": "Calculate compound interest",
    }
}
