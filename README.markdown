# 🤖 Delegent – Structured LLM Agent Framework

**Delegent** is a modular, extensible framework for building structured AI agents using LangChain. It supports custom Pydantic-based tools, multiple LLMs (e.g., Gemini, Ollama), conversational memory, and a user-friendly CLI. Designed for developers, Delegent enables rapid creation of tool-driven, conversational AI workflows with local or cloud-based models.

## 🚀 Features

- 🧠 **Structured Agents**: Powered by LangChain’s `STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION` for reliable reasoning.
- 🔌 **Custom Tools**: Define tools with Pydantic schemas and `@tool` decorator for robust input validation.
- 💬 **Conversational Memory**: Retains chat history using `ConversationBufferMemory` for context-aware interactions.
- 🌐 **LLM Flexibility**: Supports Gemini, Ollama (e.g., `llama3`, `mistral`, `phi`), and custom LLMs.
- 🖥️ **CLI Interface**: Run queries with commands like `delegent "What is AI?"`.
- ⚙️ **Environment Config**: Securely manage credentials via `.env`.
- 🛠️ **Extensible Design**: Modular structure for adding tools, agents, and LLMs.
- 📄 **MIT License**: Free for personal and commercial use.

## 📦 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/mani9441/Delegent.git
   cd Delegent
   ```

2. Install as a Python package:

   ```bash
   pip install -e .
   ```

   This makes the `delegent` CLI available globally.

3. Set up environment variables in a `.env` file (see Environment Variables).

## 🧪 Quick Start

1. Create a `.env` file in the project root:

   ```
   GOOGLE_API_KEY=your_google_genai_key
   OLLAMA_BASE_URL=http://localhost:11434
   ```

2. Run a query via CLI:

   ```bash
   delegent "What is Artificial Intelligence?"
   ```

3. Use a specific LLM:

   ```bash
   delegent "Tell me a joke" --llm ollama
   ```

### Example: Conversational Agent

Set up a conversational agent with memory and tools:

```python
from delegent.agents import centralagent
from delegent.tools.all_tools import tools
from langchain.memory import ConversationBufferMemory

# Initialize memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Combine tools (assuming additional tools in tools.all_tools)
from tools.all_tools import tools as T
tool = T + tools

# Create agent
agent = centralagent.DelegentConversationalAgent(
    structured_tools=tool,
    memory=memory,
    verbose=True
)

# Run queries
agent.run("Hi my friend")
agent.run("How do I commit a project to GitHub?")
agent.run("What did I ask you before?")
```

This agent retains conversation history and uses tools for tasks like GitHub instructions.

## 🛠️ Usage

### Basic CLI

Run queries directly:

```bash
delegent "Summarize the history of AI"
```

### Choose LLM

Specify the LLM (default is Gemini):

```bash
delegent "Explain quantum computing" --llm ollama
```

### Verbose Mode

Enable debugging output:

```bash
delegent "Search for Python news" --verbose
```

### Memory Access

Retrieve conversation history:

```python
memory.load_memory_variables({})
```

## 🧰 Available Tools

Tools are defined in `delegent/tools/` using Pydantic schemas. Example:

```python
from pydantic import BaseModel, Field
from langchain.tools import tool

class WikiInput(BaseModel):
    query: str = Field(..., description="Search query for Wikipedia")

@tool
def wiki_summary(input: WikiInput) -> str:
    """Fetches a summary from Wikipedia."""
    return wikipedia.summary(input.query)
```

To add a tool:

1. Create a tool in `delegent/tools/`.
2. Register it in `delegent/tools/all_tools.py` (e.g., `tools = [wiki_summary]`).
3. Use it via the CLI or agent.

## 🧠 Supported LLMs

- **Gemini**: Powered by `langchain-google-genai`:

  ```python
  from langchain_google_genai import ChatGoogleGenerativeAI
  ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite")
  ```

- **Ollama**: Local models via Ollama’s REST API (e.g., `llama3`, `mistral`, `phi`):

  ```python
  from delegent.llms import RemoteOllamaLLM
  ```

## 🔐 Environment Variables

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_google_genai_key
OLLAMA_BASE_URL=http://localhost:11434
```

Loaded automatically with `python-dotenv`.

## 🗂️ Project Structure

```
Delegent/
│
├── delegent/
│   ├── agents/               # Agent builder classes (e.g., DelegentConversationalAgent)
│   ├── tools/                # Pydantic-based tools
│   ├── llms/                 # LLM wrappers (Gemini, Ollama)
│   ├── __main__.py           # CLI entry point
│   ├── structuredhelper.py   # Core structured agent logic
├── setup.py                  # Package metadata
├── .gitignore                # Ignores .env, __pycache__, etc.
├── README.md                 # Project documentation
```

## 🧑‍💻 Development

### Run Locally

Test the CLI without installing:

```bash
python -m delegent "Your query here"
```

### Update and Reload

After modifying code:

```bash
pip install -e .
```

### Adding Tools or LLMs

1. Add tools to `delegent/tools/` and register in `all_tools.py`.
2. Add LLM wrappers to `delegent/llms/` and update agent logic if needed.

## 🧪 Testing

Ensure reliability:

- Create a `tests/` folder with `pytest` scripts.
- Test tools with sample inputs (e.g., `wiki_summary(WikiInput(query="Python"))`).

## 📄 License

MIT License. Free for commercial and personal use.

## 🙋‍♀️ Contributing

Contributions are welcome! See CONTRIBUTING.md for details on pull requests, bug reports, or feature suggestions.

## 📣 Author

Built by **Manikanta K**.\
*Use responsibly. Build awesomely.*