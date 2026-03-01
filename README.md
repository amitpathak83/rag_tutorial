# LearnMCP - Master the Model Context Protocol with Calculator Examples

A complete learning project demonstrating the Model Context Protocol (MCP) using calculator tools. Includes agentic workflows, MCP server implementation, and interactive demos.

## 🎯 Project Overview

This project showcases:

1. **LLM Agents** - Using LangGraph + LLM to intelligently use calculator tools
2. **Model Context Protocol** - Implementing MCP servers with FastMCP
3. **Tool Integration** - Exposing tools for remote access via MCP
4. **Interactive Demos** - User-friendly interfaces for learning

## 📁 Project Structure

```
learnmcp/
│
├── AGENT MODE (Direct LLM + Tools)
├── calculator_agent.py              ⭐ START HERE - Basic agent
├── advanced_calculator.py           • Extended agent with more features
├── interactive_calculator.py        • Interactive chat mode
│
├── MCP MODE (Protocol-based)
├── mcp_calculator_server.py         ⭐ FastMCP server implementation
├── MCP_SETUP.md                     • Detailed MCP documentation
├── MCP_EXAMPLES.md                  • Integration examples
│
├── DOCUMENTATION
├── README.md                        ← You are here
├── quick_start.py                   • Quick reference guide
├── startup.py                       • Setup checker & guide
│
└── CONFIGURATION
    └── Pipfile                      • Python dependencies
```

## 🚀 Quick Start

### Option 1: Run Agent Examples (Simplest)

**Prerequisites:**
- Ollama running: `ollama serve` (in another terminal)
- Model downloaded: `ollama pull llama3.2`

**Run:**
```bash
pipenv install
pipenv shell
python calculator_agent.py          # Run examples
python interactive_calculator.py    # Interactive chat
```

### Option 2: Run MCP Server (Most Scalable)

**Prerequisites:**
- Same as above

**Run:**
```bash
pipenv install
pipenv shell
python mcp_calculator_server.py     # Start server
# Server runs and waits for MCP clients
```

Then connect with Claude or another MCP-compatible client.

## 📚 Learning Path

### Beginner: Understanding Agents

1. **Read**: Look at the comments in `calculator_agent.py`
2. **Run**: `python calculator_agent.py`
3. **Understand**: How LLM calls tools, processes results, and answers questions
4. **Experiment**: Modify tool definitions or add new ones

### Intermediate: Making It Interactive

1. **Run**: `python interactive_calculator.py`
2. **Try**: Ask various math questions
3. **Observe**: How different query types are handled
4. **Learn**: LLM reasoning and tool selection

###Advanced: Understanding MCP

1. **Read**: `MCP_SETUP.md` for protocol details
2. **Run**: `python mcp_calculator_server.py`
3. **Understand**: How FastMCP exposes tools via MCP
4. **Extend**: Add new tools and rebuild the server

### Expert: Building Your Own MCP Server

1. **Study**: `mcp_calculator_server.py` structure
2. **Create**: Your own domain-specific MCP server
3. **Deploy**: To production with proper error handling
4. **Integrate**: With Claude or other LLM applications

## 💡 Key Concepts

### LLM Agents (calculator_agent.py)

```
Input Query → LLM → Tool Selection → Tool Execution 
→ Result Processing → LLM → Final Answer
```

**Benefits:**
- Direct Python function calls
- Minimal latency
- Perfect for single-process apps
- Easy debugging

### MCP Server (mcp_calculator_server.py)

```
LLM Client → stdio → MCP Server → Tool Execution → Result
```

**Benefits:**
- Distributed architecture
- Language-agnostic protocol
- Integrates with Claude natively
- Scalable and maintainable

## 🔧 Available Tools

All modes support these 10 calculator tools:

| Function | Use | Example |
|----------|-----|---------|
| `add` | Addition | 5 + 3 = 8 |
| `subtract` | Subtraction | 100 - 25 = 75 |
| `multiply` | Multiplication | 12 × 8 = 96 |
| `divide` | Division | 144 ÷ 12 = 12 |
| `power` | Exponentiation | 2^10 = 1024 |
| `square_root` | Square root | √144 = 12 |
| `percentage` | Percentages | 20% of 500 = 100 |
| `modulo` | Remainders | 17 mod 5 = 2 |
| `average` | Averaging | avg(10,20,30) = 20 |
| `factorial` | Factorial | 5! = 120 |

## 🎮 Example Queries

Try asking the agent:
- "What is 25 plus 17?"
- "Multiply 12 by 8"
- "What is 2 to the power of 10?"
- "Calculate 20% of 500"
- "What's the average of 10, 20, 30?"

## 🔗 Integration with Ollama

This project uses **Ollama** for local LLM inference:

### Set Up Ollama

```bash
# Install (macOS)
brew install ollama

# Or download from https://ollama.ai

# Start it
ollama serve

# Download a model (new terminal)
ollama pull mistral      # Fast & good
ollama pull neural-chat  # Conversation optimized
ollama pull phi          # Ultra fast (small)
```

### Configure in Code

Edit model in `calculator_agent.py` or `advanced_calculator.py`:
```python
llm = ChatOllama(
    model="mistral",  # Change this
    temperature=0.7,
    base_url="http://localhost:11434",
)
```

## 📊 Comparison: Agent vs MCP

| Aspect | Agent | MCP |
|--------|-------|-----|
| Setup Complexity | Simple | Medium |
| Startup Time | Instant | <100ms |
| Overhead | Low | Low |
| Scalability | Single process | Distributed |
| Integration | LangChain-only | Any MCP client |
| Best For | Early dev, demos | Production, Claude |

## 🛠️ Configuration & Extensions

### Add a New Tool

**For Agent Mode:**
```python
@tool
def logarithm(n:  float, base: float = 10) -> float:
    """Calculate logarithm."""
    import math
    return math.log(n, base)

# Add to tools list
tools = [..., logarithm]
```

**For MCP Mode:**
```python
@mcp.tool()
def logarithm(n: float, base: float = 10) -> float:
    """Calculate logarithm."""
    import math
    return math.log(n, base)
```

### Change LLM Model

Edit any Python file to use a different Ollama model:
```python
llm = ChatOllama(
    model="neural-chat",      # ← change this
    temperature=0.5,
    base_url="http://localhost:11434",
)
```

## 📖 Documentation Files

- **README.md** (this file) - Project overview
- **MCP_SETUP.md** - Detailed MCP protocol & server documentation
- **MCP_EXAMPLES.md** - Integration examples & use cases
- **quick_start.py** - Quick reference guide
- **startup.py** - Setup checker & interactive guide

## ⚙️ System Requirements

- **Python**: 3.10 or higher
- **Ollama**: For LLM operations (agent mode only)
- **Ram**: 2GB+ (Ollama) + 500MB (project)
- **Disk**: 5GB+ (Ollama models) + 100MB (project)
- **OS**: macOS, Linux, Windows (with WSL)

## 📦 Dependencies

Main packages (in Pipfile):
- `mcp` - Model Context Protocol
- `langchain-ollama` - Ollama integration
- `langgraph` - Agent orchestration
- `langchain-core` - LangChain foundation

Install with: `pipenv install`

## 🧪 Testing

### Test Agent
```bash
python calculator_agent.py
# Should run example queries
```

### Test MCP Server
```bash
python mcp_calculator_server.py
# Should start and wait for connections
```

### Test Interactive Mode
```bash
python interactive_calculator.py
# Should launch interactive prompt
```

## 🚨 Troubleshooting

### "Connection refused" (Ollama)
```bash
# Check if Ollama is running
ps aux | grep ollama

# Start it
ollama serve
```

### "Model not found"
```bash
# Download the model
ollama pull mistral
```

### "Module not found"
```bash
# Install dependencies
pipenv install

# Activate environment
pipenv shell
```

### MCP Server won't start
```bash
# Check Python version
python --version  # 3.10+ required

# Run with verbose output
python -u mcp_calculator_server.py
```

## 🎓 Learning Resources

### Internal
- Study `calculator_agent.py` comments for agent concepts
- Read `mcp_calculator_server.py` for MCP server patterns
- Try `advanced_calculator.py` for complex workflows

### External
- [MCP Specification](https://spec.modelcontextprotocol.io)
- [LangChain Docs](https://python.langchain.com)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph)
- [Ollama Docs](https://ollama.ai)

## 🤝 Contributing

To extend this project:

1. Add tools to `CalculatorTools` class
2. Register in `tools` list (agent) or as `@mcp.tool()` (MCP)
3. Update tool schemas if needed
4. Test with example queries

## 📝 File Descriptions

| File | Purpose | Lines |
|------|---------|-------|
| calculator_agent.py | Basic agent with LangGraph | ~240 |
| advanced_calculator.py | Extended agents with more tools | ~350 |
| interactive_calculator.py | User-friendly chat interface | ~70 |
| mcp_calculator_server.py | FastMCP server implementation | ~150 |
| quick_start.py | Quick reference guide | ~100 |
| startup.py | Setup checker & interactive guide | ~400 |

## 🎯 Next Steps

1. **Get Started**: Run `python startup.py` for setup guide
2. **Try Agent Mode**: `python calculator_agent.py`
3. **Try Interactive**: `python interactive_calculator.py`
4. **Learn MCP**: Read `MCP_SETUP.md`
5. **Run MCP Server**: `python mcp_calculator_server.py`
6. **Extend**: Add custom tools
7. **Deploy**: Use in production application

## 📄 License

Educational - Use freely for learning!

## 🎉 Summary

This project demonstrates:

✅ LLM Agents with tool use (LangGraph)  
✅ Model Context Protocol implementation (FastMCP)  
✅ Integration with local LLMs (Ollama)  
✅ Interactive user interfaces  
✅ Protocol-based tool access  
✅ Best practices for agentic architectures  

Perfect for learning or building production MCP servers!

---

**Created**: March 2026  
**Python**: 3.10+  
**Framework**: LangChain, LangGraph, FastMCP  
**LLM**: Ollama (local)
Use any PDF
