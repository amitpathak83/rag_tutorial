#!/usr/bin/env python3
"""
MCP Project Quick Start & Configuration
Setup and running instructions for the complete MCP implementation.
"""

import subprocess
import sys
import os
from pathlib import Path


def print_header(title: str):
    """Print a formatted header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def check_dependencies():
    """Check if all required dependencies are installed."""
    print_header("Checking Dependencies")

    required_packages = [
        ("mcp", "Model Context Protocol"),
        ("langchain_ollama", "LangChain Ollama"),
        ("langchain_core", "LangChain Core"),
        ("langgraph", "LangGraph"),
    ]

    missing = []

    for package, name in required_packages:
        try:
            __import__(package)
            print(f"✓ {name} installed")
        except ImportError:
            print(f"✗ {name} missing")
            missing.append(package)

    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("Installing missing packages...")
        subprocess.run(["pipenv", "install", *missing], check=False)
    else:
        print("\n✓ All dependencies installed")

    return len(missing) == 0


def check_ollama():
    """Check if Ollama is installed and running."""
    print_header("Checking Ollama")

    try:
        import requests
        response = requests.get(
            "http://localhost:11434/api/version", timeout=2)
        print("✓ Ollama is running")
        return True
    except Exception:
        print("✗ Ollama is not running")
        print("\nTo start Ollama:")
        print("  $ ollama serve")
        print("\nTo download a model:")
        print("  $ ollama pull mistral")
        return False


def show_project_structure():
    """Show the project structure."""
    print_header("Project Structure")

    structure = """
learnmcp/
├── HelloMCP.py
├── Pipfile                          # Python dependencies
├── 
├── CORE AGENT
├── calculator_agent.py              # Basic calculator agent with LangGraph
├── advanced_calculator.py           # Extended agent with more tools
├── interactive_calculator.py        # Interactive chat interface
│
├── MCP IMPLEMENTATION
├── mcp_calculator_server.py         # MCP Server (exposes tools)
├── mcp_calculator_client.py         # MCP Client (connects to server)
├── mcp_agent_integration.py         # Integrate MCP with LLM agent
│
├── DOCUMENTATION
├── README.md                        # General project overview
├── MCP_SETUP.md                     # MCP documentation
├── quick_start.py                   # Quick start guide
└── startup.py                       # This file

Available Ways to Run:

1. CALCULATOR AGENT (Standalone LLM Agent)
   python calculator_agent.py              # Run with examples
   python interactive_calculator.py        # Interactive mode
   python advanced_calculator.py demo1     # Run demos

2. MCP SERVER + CLIENT (Protocol-based)
   Terminal 1: python mcp_calculator_server.py
   Terminal 2: python mcp_calculator_client.py
   Terminal 2: python mcp_calculator_client.py demo

3. MCP + AGENT INTEGRATION
   Terminal 1: python mcp_calculator_server.py
   Terminal 2: python mcp_agent_integration.py
    """

    print(structure)


def show_quick_commands():
    """Show quick commands."""
    print_header("Quick Commands")

    commands = """
SETUP:
  pipenv install                      # Install dependencies
  ollama serve                        # Start Ollama (keep running)
  ollama pull mistral                 # Download model

AGENT MODE:
  python calculator_agent.py          # Run basic agent
  python interactive_calculator.py    # Interactive agent
  python advanced_calculator.py demo  # Run advanced demos

MCP MODE:
  python mcp_calculator_server.py     # Start MCP server
  python mcp_calculator_client.py     # Connect client (interactive)
  python mcp_calculator_client.py demo # Run client demos

INTEGRATION:
  python mcp_agent_integration.py     # Run agent with MCP tools

DOCUMENTATION:
  python quick_start.py               # Quick start guide
  cat README.md                       # General overview
  cat MCP_SETUP.md                    # MCP documentation
    """

    print(commands)


def show_feature_comparison():
    """Show comparison of different modes."""
    print_header("Feature Comparison")

    comparison = """
MODE                    | Local Only | Tool Access | Protocol | Use Case
─────────────────────────────────────────────────────────────────────────
Calculator Agent        | Yes        | Yes         | Direct   | Simple demos
Interactive Agent       | Yes        | Yes         | Direct   | User queries
Advanced Agent          | Yes        | Yes+        | Direct   | Complex math
MCP Server/Client       | No         | Yes         | MCP      | Distributed
Agent + MCP             | No         | Yes         | MCP+LLM  | Integrated

* Local Only: Runs entirely on your machine
* Tool Access: Can call calculator functions
* Protocol: Communication method (Direct = function calls, MCP = network protocol)
* Advanced: Includes financial calculations, statistical operations

KEY DIFFERENCES:

Calculator Agent:
  - Direct Python function calls
  - Single process
  - Fast & lightweight
  - No network overhead

MCP Server/Client:
  - Protocol-based communication
  - Can run separately
  - Extensible & scalable
  - Follows Model Context Protocol spec
  - Can integrate with multiple clients

Agent + MCP:
  - Best of both worlds
  - LLM agent uses MCP tools
  - Allows distributed tool access
  - Can connect to external MCP servers
    """

    print(comparison)


def show_examples():
    """Show example usage."""
    print_header("Example Queries")

    examples = """
BASIC MATH:
  "What is 25 plus 17?"
  "Calculate 100 minus 35"
  "Multiply 12 by 8"
  "What is 144 divided by 12?"

ADVANCED MATH:
  "What is 2 to the power of 10?"
  "What is the square root of 144?"
  "What is the factorial of 5?"
  "Calculate the average of 10, 20, 30, 40, 50"

FINANCIAL:
  "Calculate 20% of 500"
  "What percentage is 25 out of 200?"
  "If I invest $1000 at 5% for 2 years, how much will I have?"

MULTI-STEP:
  "What is (25 + 17) × 2?"
  "Calculate 20% of 500, then divide by 5"
  "If I add 10, 20, and 30, what's the average?"
    """

    print(examples)


def show_troubleshooting():
    """Show troubleshooting guide."""
    print_header("Troubleshooting")

    troubleshooting = """
OLLAMA ISSUES:

  Error: "Connection refused"
    → Make sure Ollama is running: ollama serve
    → Check it's on http://localhost:11434

  Error: "Model not found"
    → Download the model: ollama pull mistral
    → Or use a different model: ollama pull neural-chat

  Slow responses
    → Try a smaller model: ollama pull neural-chat
    → Or: ollama pull phi
    → Adjust temperature parameter (0.3 = faster, 0.7 = slower)

PYTHON ISSUES:

  Error: "Module not found"
    → Install dependencies: pipenv install
    → Activate environment: pipenv shell

  ImportError for langchain/langgraph
    → Update dependencies: pipenv update
    → Reinstall: pipenv install --ignore-pipfile

MCP ISSUES:

  Client/Server won't connect
    → Make sure server is running in another terminal
    → Check server output for startup messages
    → Use: python mcp_calculator_server.py (verbose)

  Agent with MCP not working
    → Both Ollama and MCP server must be running
    → Check both are on expected ports

PERFORMANCE:

  Agent is slow
    → Ollama response time depends on model and hardware
    → Mistral is fastest on most machines
    → Try: ollama pull mistral:7b (smaller version)
    
  Many iterations/tool calls
    → Reduce temperature (0.3 for focused reasoning)
    → Use simpler model (neural-chat)
    """

    print(troubleshooting)


def show_next_steps():
    """Show next steps."""
    print_header("Next Steps")

    next_steps = """
1. SETUP:
   ✓ Check dependencies: Run 'python startup.py' (this script)
   ✓ Install packages: pipenv install
   ✓ Start Ollama: ollama serve (in another terminal)
   ✓ Download model: ollama pull mistral

2. TRY THE AGENT:
   ✓ Run: python calculator_agent.py
   ✓ Or: python interactive_calculator.py
   ✓ Or: python advanced_calculator.py demo

3. TRY THE MCP IMPLEMENTATION:
   ✓ Terminal 1: python mcp_calculator_server.py
   ✓ Terminal 2: python mcp_calculator_client.py demo
   ✓ Or interactive: python mcp_calculator_client.py

4. TRY THE INTEGRATION:
   ✓ Terminal 1: python mcp_calculator_server.py
   ✓ Terminal 2: ollama serve (if not already running)
   ✓ Terminal 3: python mcp_agent_integration.py

5. CUSTOMIZE:
   ✓ Add more tools to calculator_agent.py
   ✓ Extend MCP server with new operations
   ✓ Create your own MCP server for different domain
   ✓ Integrate with other LLM frameworks

6. LEARN MORE:
   ✓ Read: README.md
   ✓ Read: MCP_SETUP.md
   ✓ Read: quick_start.py
   ✓ Visit: https://modelcontextprotocol.io
    """

    print(next_steps)


def main():
    """Main startup flow."""
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║                  LEARN MCP - PROJECT STARTUP GUIDE                      ║
║                                                                          ║
║    Master the Model Context Protocol with Calculator Examples           ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)

    import argparse

    parser = argparse.ArgumentParser(description="MCP Project Startup Guide")
    parser.add_argument("--check", action="store_true",
                        help="Check dependencies")
    parser.add_argument("--ollama", action="store_true", help="Check Ollama")
    parser.add_argument("--structure", action="store_true",
                        help="Show project structure")
    parser.add_argument("--commands", action="store_true",
                        help="Show quick commands")
    parser.add_argument("--compare", action="store_true",
                        help="Compare features")
    parser.add_argument("--examples", action="store_true",
                        help="Show examples")
    parser.add_argument("--troubleshoot", action="store_true",
                        help="Show troubleshooting")
    parser.add_argument("--all", action="store_true",
                        help="Show all information")

    args = parser.parse_args()

    if args.all or (not any([args.check, args.ollama, args.structure, args.commands,
                            args.compare, args.examples, args.troubleshoot])):
        # Default: show all
        check_dependencies()
        check_ollama()
        show_project_structure()
        show_quick_commands()
        show_feature_comparison()
        show_examples()
        show_next_steps()
    else:
        if args.check:
            check_dependencies()
        if args.ollama:
            check_ollama()
        if args.structure:
            show_project_structure()
        if args.commands:
            show_quick_commands()
        if args.compare:
            show_feature_comparison()
        if args.examples:
            show_examples()
        if args.troubleshoot:
            show_troubleshooting()

    print("\n" + "="*70)
    print("For more information, see:")
    print("  - README.md (project overview)")
    print("  - MCP_SETUP.md (MCP documentation)")
    print("  - quick_start.py (quick reference)")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
