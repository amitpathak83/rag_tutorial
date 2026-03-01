#!/usr/bin/env python3
"""
LangChain Prompt Client with Ollama (llama3.2)
Demonstrates various LLM parameters: temperature, top_k, top_p, etc.
"""

from langchain_ollama import ChatOllama, OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import sys


class PromptClient:
    """Simple prompt client with configurable LLM parameters."""

    def __init__(
        self,
        model: str = "llama3.2",
        temperature: float = 0.5,
        top_k: int = 40,
        top_p: float = 0.9,
        num_predict: int = 128,
        num_ctx: int = 2048,
        repeat_penalty: float = 1.1,
    ):
        """
        Initialize the prompt client with LLM parameters.

        Args:
            model: Ollama model name (default: llama3.2)
            temperature: Controls randomness (0.0-1.0)
                - 0.0 = deterministic/focused
                - 0.5 = balanced (default)
                - 1.0 = creative/random
            top_k: Keep only top k most likely tokens (0 disables)
            top_p: Nucleus sampling (0.0-1.0)
                - 0.9 = keep top 90% probability mass (default)
                - Lower = more focused
                - Higher = more diverse
            num_predict: Maximum tokens to generate
            num_ctx: Context window size
            repeat_penalty: Penalizes repetition (1.0 = no penalty)
        """
        self.model = model
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p
        self.num_predict = num_predict
        self.num_ctx = num_ctx
        self.repeat_penalty = repeat_penalty

        # Initialize ChatOllama with parameters
        self.llm = ChatOllama(
            model=model,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            num_predict=num_predict,
            num_ctx=num_ctx,
            repeat_penalty=repeat_penalty,
        )

        print(f"✓ Initialized {model} with:")
        print(f"  - Temperature: {temperature}")
        print(f"  - Top K: {top_k}")
        print(f"  - Top P: {top_p}")
        print(f"  - Max tokens: {num_predict}")
        print(f"  - Context window: {num_ctx}")
        print(f"  - Repeat penalty: {repeat_penalty}\n")

    def prompt(self, text: str) -> str:
        """Send a simple text prompt and get response."""
        response = self.llm.invoke(text)
        return response.content

    def chat_prompt(self, system: str, user: str) -> str:
        """Send a chat-style prompt with system and user message."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", system),
            ("user", user)
        ])
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({})

    def template_prompt(self, template: str, **variables) -> str:
        """Send a templated prompt with variables."""
        prompt = PromptTemplate(
            template=template,
            input_variables=list(variables.keys())
        )
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke(variables)

    def update_parameters(self, **kwargs):
        """Update LLM parameters."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        # Reinitialize with new parameters
        self.llm = ChatOllama(
            model=self.model,
            temperature=self.temperature,
            top_k=self.top_k,
            top_p=self.top_p,
            num_predict=self.num_predict,
            num_ctx=self.num_ctx,
            repeat_penalty=self.repeat_penalty,
        )
        print(f"✓ Updated parameters\n")


def example_1_basic_prompt():
    """Example 1: Basic prompt with default parameters."""
    print("="*60)
    print("Example 1: Basic Prompt (Balanced - Temperature=0.5)")
    print("="*60 + "\n")

    client = PromptClient()

    prompt = "Explain quantum computing in 3 sentences."
    print(f"Prompt: {prompt}\n")
    response = client.prompt(prompt)
    print(f"Response:\n{response}\n")


def example_2_temperature_comparison():
    """Example 2: Compare different temperatures."""
    print("="*60)
    print("Example 2: Temperature Comparison")
    print("="*60 + "\n")

    prompt = "Complete this sentence: The future of AI is..."

    temperatures = [0.1, 0.3, 0.7, 1.0]

    for temp in temperatures:
        client = PromptClient(temperature=temp)
        print(f"\n--- Temperature: {temp} (", end="")
        if temp < 0.3:
            print("Very Focused) ---")
        elif temp < 0.5:
            print("Focused) ---")
        elif temp < 0.8:
            print("Balanced) ---")
        else:
            print("Creative) ---")

        response = client.prompt(prompt)
        print(f"Response: {response}\n")


def example_3_top_k_p_sampling():
    """Example 3: Top-k and Top-p sampling."""
    print("="*60)
    print("Example 3: Sampling Strategies (Top-k vs Top-p)")
    print("="*60 + "\n")

    prompt = "Write a creative sentence about nature."

    # Top-k only (restricts vocabulary)
    print("--- Strategy 1: Top-k=20 (Restrictive) ---")
    client = PromptClient(top_k=20, top_p=1.0, temperature=0.8)
    response = client.prompt(prompt)
    print(f"Response: {response}\n")

    # Top-p only (nucleus sampling)
    print("--- Strategy 2: Top-p=0.7 (Nucleus Sampling - Focused) ---")
    client = PromptClient(top_k=0, top_p=0.7, temperature=0.8)
    response = client.prompt(prompt)
    print(f"Response: {response}\n")

    # Top-p higher (more diverse)
    print("--- Strategy 3: Top-p=0.95 (More Diverse) ---")
    client = PromptClient(top_k=0, top_p=0.95, temperature=0.8)
    response = client.prompt(prompt)
    print(f"Response: {response}\n")


def example_4_chat_format():
    """Example 4: Chat-style prompts with system message."""
    print("="*60)
    print("Example 4: Chat Format (System + User)")
    print("="*60 + "\n")

    client = PromptClient(temperature=0.7)

    # Expert chatbot
    print("--- Expert Python Programmer ---")
    response = client.chat_prompt(
        system="You are an expert Python programmer. Answer questions clearly and concisely.",
        user="What is a list comprehension?"
    )
    print(f"Response: {response}\n")

    # Casual assistant
    print("--- Casual Friend ---")
    client.update_parameters(temperature=0.9)
    response = client.chat_prompt(
        system="You are a casual, friendly assistant who uses humor and emojis.",
        user="What's a fun Python trick?"
    )
    print(f"Response: {response}\n")


def example_5_templated_prompt():
    """Example 5: Templated prompts with variables."""
    print("="*60)
    print("Example 5: Templated Prompts")
    print("="*60 + "\n")

    client = PromptClient(temperature=0.6)

    # Example 1: Story prompt
    template = """Create a short {length} story about a {character} who {action}.
Make it {tone}."""

    print("--- Generate a short story ---")
    response = client.template_prompt(
        template=template,
        length="2-3 sentence",
        character="curious robot",
        action="discovers an old library",
        tone="mysterious and intriguing"
    )
    print(f"Response: {response}\n")

    # Example 2: Code generation
    template = """Write a {language} function that {task}.
Only show the code, no explanation."""

    print("--- Generate Python code ---")
    response = client.template_prompt(
        template=template,
        language="Python",
        task="sorts a list in reverse order"
    )
    print(f"Response: {response}\n")


def example_6_output_length_control():
    """Example 6: Control output length with num_predict."""
    print("="*60)
    print("Example 6: Output Length Control (num_predict)")
    print("="*60 + "\n")

    prompt = "What is machine learning?"

    # Short response
    print("--- Short response (30 tokens max) ---")
    client = PromptClient(num_predict=30)
    response = client.prompt(prompt)
    print(f"Response: {response}\n")

    # Medium response
    print("--- Medium response (100 tokens max) ---")
    client.update_parameters(num_predict=100)
    response = client.prompt(prompt)
    print(f"Response: {response}\n")

    # Long response
    print("--- Long response (300 tokens max) ---")
    client.update_parameters(num_predict=300)
    response = client.prompt(prompt)
    print(f"Response: {response}\n")


def example_7_repeat_penalty():
    """Example 7: Control repetition with repeat_penalty."""
    print("="*60)
    print("Example 7: Repetition Control (repeat_penalty)")
    print("="*60 + "\n")

    prompt = "List 5 creative uses for artificial intelligence:"

    # Low penalty (allow repetition)
    print("--- Low penalty (1.0 - Allow repetition) ---")
    client = PromptClient(repeat_penalty=1.0, num_predict=150)
    response = client.prompt(prompt)
    print(f"Response: {response}\n")

    # High penalty (avoid repetition)
    print("--- High penalty (1.2 - Avoid repetition) ---")
    client.update_parameters(repeat_penalty=1.2)
    response = client.prompt(prompt)
    print(f"Response: {response}\n")


def interactive_mode():
    """Interactive mode for experimenting with parameters."""
    print("="*60)
    print("Interactive Prompt Client")
    print("="*60)
    print("\nInitialize with default parameters...")

    client = PromptClient(
        model="llama3.2",
        temperature=0.5,
        top_k=40,
        top_p=0.9,
        num_predict=200,
    )

    print("\nAvailable commands:")
    print("  prompt <text>              - Send a prompt")
    print("  chat <system> | <user>     - Send a chat prompt")
    print("  temp <value>               - Change temperature (0.0-1.0)")
    print("  topk <value>               - Change top-k")
    print("  topp <value>               - Change top-p")
    print("  maxlen <value>             - Change max tokens")
    print("  config                     - Show current config")
    print("  examples                   - Show all examples")
    print("  quit                       - Exit\n")

    while True:
        try:
            user_input = input(">> ").strip()

            if not user_input:
                continue

            if user_input.lower() == "quit":
                print("Goodbye!")
                break

            if user_input.lower() == "config":
                print(f"\nCurrent Configuration:")
                print(f"  Model: {client.model}")
                print(f"  Temperature: {client.temperature}")
                print(f"  Top-k: {client.top_k}")
                print(f"  Top-p: {client.top_p}")
                print(f"  Max tokens: {client.num_predict}")
                print(f"  Context: {client.num_ctx}")
                print(f"  Repeat penalty: {client.repeat_penalty}\n")
                continue

            if user_input.lower() == "examples":
                print("\nRun examples with:")
                print("  python prompt_client.py --example1  (Basic prompt)")
                print("  python prompt_client.py --example2  (Temperature)")
                print("  python prompt_client.py --example3  (Sampling)")
                print("  python prompt_client.py --example4  (Chat format)")
                print("  python prompt_client.py --example5  (Templates)")
                print("  python prompt_client.py --example6  (Output length)")
                print("  python prompt_client.py --example7  (Repetition)")
                print()
                continue

            if user_input.lower().startswith("prompt "):
                prompt_text = user_input[7:]
                print(f"\nResponse:\n{client.prompt(prompt_text)}\n")

            elif user_input.lower().startswith("chat "):
                parts = user_input[5:].split(" | ")
                if len(parts) == 2:
                    response = client.chat_prompt(
                        parts[0].strip(), parts[1].strip())
                    print(f"\nResponse:\n{response}\n")
                else:
                    print("Usage: chat <system message> | <user message>\n")

            elif user_input.lower().startswith("temp "):
                try:
                    temp = float(user_input[5:])
                    if 0.0 <= temp <= 1.0:
                        client.update_parameters(temperature=temp)
                    else:
                        print("Temperature must be between 0.0 and 1.0\n")
                except ValueError:
                    print("Invalid temperature value\n")

            elif user_input.lower().startswith("topk "):
                try:
                    topk = int(user_input[5:])
                    client.update_parameters(top_k=topk)
                except ValueError:
                    print("Invalid top-k value\n")

            elif user_input.lower().startswith("topp "):
                try:
                    topp = float(user_input[5:])
                    if 0.0 <= topp <= 1.0:
                        client.update_parameters(top_p=topp)
                    else:
                        print("Top-p must be between 0.0 and 1.0\n")
                except ValueError:
                    print("Invalid top-p value\n")

            elif user_input.lower().startswith("maxlen "):
                try:
                    maxlen = int(user_input[7:])
                    client.update_parameters(num_predict=maxlen)
                except ValueError:
                    print("Invalid max length value\n")

            else:
                print("Unknown command. Type 'quit' to exit.\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()

        if arg == "--example1":
            example_1_basic_prompt()
        elif arg == "--example2":
            example_2_temperature_comparison()
        elif arg == "--example3":
            example_3_top_k_p_sampling()
        elif arg == "--example4":
            example_4_chat_format()
        elif arg == "--example5":
            example_5_templated_prompt()
        elif arg == "--example6":
            example_6_output_length_control()
        elif arg == "--example7":
            example_7_repeat_penalty()
        elif arg == "--interactive":
            interactive_mode()
        elif arg == "--all":
            print("\n" + "="*60)
            print("RUNNING ALL EXAMPLES")
            print("="*60 + "\n")
            example_1_basic_prompt()
            input("\nPress Enter for next example...")
            example_2_temperature_comparison()
            input("\nPress Enter for next example...")
            example_3_top_k_p_sampling()
            input("\nPress Enter for next example...")
            example_4_chat_format()
            input("\nPress Enter for next example...")
            example_5_templated_prompt()
            input("\nPress Enter for next example...")
            example_6_output_length_control()
            input("\nPress Enter for next example...")
            example_7_repeat_penalty()
            print("\n✓ All examples completed!")
        else:
            print(f"Unknown option: {arg}")
            print_help()
    else:
        print_help()


def print_help():
    """Print help information."""
    print("""
╔════════════════════════════════════════════════════════════════╗
║     LangChain Prompt Client with Ollama (llama3.2)            ║
╚════════════════════════════════════════════════════════════════╝

USAGE:
  python prompt_client.py [option]

OPTIONS:
  --example1          Basic prompt with default parameters
  --example2          Temperature comparison (0.1 to 1.0)
  --example3          Sampling strategies (top-k vs top-p)
  --example4          Chat format with system message
  --example5          Templated prompts with variables
  --example6          Output length control (num_predict)
  --example7          Repetition control (repeat_penalty)
  --all              Run all examples (interactive)
  --interactive      Interactive prompt client (REPL mode)

PARAMETER EXPLANATION:

Temperature (0.0-1.0):
  0.0 = Deterministic, focused, repeated answers
  0.5 = Balanced (default)
  1.0 = Creative, random, diverse

Top-k (integer, 0=disabled):
  Restricts choices to top-k most likely tokens
  Lower = more focused, Higher = more diverse
  Common: 20-50

Top-p (0.0-1.0):
  Nucleus sampling - keeps top p% probability mass
  0.7 = Focused, 0.9 = Balanced (default), 0.95+ = Diverse
  Works well with lower temperature

num_predict (integer):
  Maximum tokens to generate (roughly words × 0.75)
  Common: 50-500

repeat_penalty (float):
  1.0 = No penalty, 1.2 = Avoid repetition
  Higher = penalize repeated tokens more

QUICK START:
  1. Run example 1:      python prompt_client.py --example1
  2. Run temperature:    python prompt_client.py --example2
  3. Interactive mode:   python prompt_client.py --interactive
  4. Run all:            python prompt_client.py --all

INTERACTIVE COMMANDS:
  prompt <text>         Send a simple prompt
  chat <sys> | <user>   Send a chat prompt
  temp <value>          Set temperature
  topk <value>          Set top-k
  topp <value>          Set top-p
  maxlen <value>        Set max tokens
  config                Show current settings
  examples              Show example commands
  quit                  Exit

REQUIREMENTS:
  - Ollama running: ollama serve
  - llama3.2 model: ollama pull llama3.2
  - LangChain: pip install langchain-ollama

EXAMPLES:
  # Basic prompt
  $ python prompt_client.py --example1

  # Compare temperatures
  $ python prompt_client.py --example2

  # Interactive REPL
  $ python prompt_client.py --interactive
  >> prompt What is Python?
  >> temp 0.9
  >> topk 20
  >> prompt Write a poem

AUTHOR: AI Assistant
LICENSE: Open Source
""")


if __name__ == "__main__":
    main()
