# Contributing to Delegent

Thank you for your interest in contributing to **Delegent**, a modular framework for building structured LLM agents with LangChain! We welcome contributions from the community to enhance features, fix bugs, or improve documentation.

## 🌟 How to Contribute

### 1. Fork the Repository

- Click the "Fork" button on the [Delegent GitHub page](https://github.com/mani9441/Delegent).
- Clone your fork to your local machine:
  ```bash
  git clone https://github.com/yourusername/Delegent.git
  cd Delegent
  ```

### 2. Set Up the Environment

- Install dependencies:
  ```bash
  pip install -e .
  ```
- Create a `.env` file for credentials (e.g., `GOOGLE_API_KEY`, `OLLAMA_BASE_URL`):
  ```
  GOOGLE_API_KEY=your_google_genai_key
  OLLAMA_BASE_URL=http://localhost:11434
  ```

### 3. Create a Branch

- Create a new branch for your changes:
  ```bash
  git checkout -b feature/your-feature-name
  ```
  Use descriptive names (e.g., `feature/add-web-scraper-tool`, `fix/cli-error-handling`).

### 4. Make Changes

- **Code**: Add or modify files in `delegent/agents/`, `delegent/tools/`, or `delegent/llms/`.
- **Tools**: Define new tools in `delegent/tools/` with Pydantic schemas and register them in `delegent/tools/all_tools.py`.
- **Tests**: Add tests in a `tests/` folder (use `pytest`).
- **Docs**: Update `README.md` or other documentation as needed.

### 5. Test Your Changes

- Run the CLI to verify:
  ```bash
  python -m delegent "Test query"
  ```
- For conversational agents, test with memory:

  ```python
  from delegent.agents import centralagent
  from delegent.tools.all_tools import tools
  from langchain.memory import ConversationBufferMemory

  memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
  agent = centralagent.DelegentConversationalAgent(structured_tools=tools, memory=memory, verbose=True)
  agent.run("Test your feature")
  ```

- Ensure no errors with tools or LLMs (e.g., Gemini, Ollama).

### 6. Commit and Push

- Format code with `black`:
  ```bash
  black .
  ```
- Write clear commit messages:
  ```bash
  git commit -m "Add web scraper tool with Pydantic schema"
  ```
- Push your branch:
  ```bash
  git push origin feature/your-feature-name
  ```

### 7. Submit a Pull Request

- Create a pull request (PR) on the [Delegent repository](https://github.com/mani9441/Delegent).
- Include a clear description of your changes, referencing any related issues.
- Ensure your PR passes any CI checks (if set up).

## 📏 Guidelines

- **Code Style**: Follow PEP 8 and use `black` for formatting.
- **Commits**: Write concise, descriptive commit messages (e.g., `Fix bug in Ollama LLM wrapper`).
- **Testing**: Test tools and agents locally. Add unit tests for new features.
- **Tools**: Define tools with Pydantic schemas in `delegent/tools/` and register in `all_tools.py`.
- **Documentation**: Update `README.md` or add docstrings for new code.
- **Respect**: Be kind and collaborative in discussions.

## 🐛 Reporting Bugs

- Open an issue on the [GitHub Issues page](https://github.com/mani9441/Delegent/issues).
- Provide:
  - A clear title (e.g., `CLI crashes with invalid LLM option`).
  - Steps to reproduce, expected behavior, and actual behavior.
  - Relevant logs or screenshots.

## 💡 Suggesting Features

- Open an issue with the label “enhancement.”
- Describe the feature, its use case, and potential implementation ideas.

## 🛠️ Development Tips

- **Tools**: Add new tools to `delegent/tools/` (e.g., a web scraper or API caller) and update `all_tools.py`.
- **LLMs**: Extend `delegent/llms/` for new models, ensuring compatibility with `centralagent`.
- **Memory**: Test conversational features with `ConversationBufferMemory` for context retention.
- **Debugging**: Use `--verbose` in CLI or `verbose=True` in agents for detailed logs.

## 📬 Contact

For questions, reach out via GitHub Issues or k.manikanta9441@gmail.com.

Thank you for contributing to **Delegent**! Let’s build awesome AI agents together. 🚀
