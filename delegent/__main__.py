# delegent/__main__.py
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import FileChatMessageHistory

import sys
import argparse
from delegent.agents.centralagent import DelegentConversationalAgent
from delegent.tools import all_tools  # Your tool list here



memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    chat_memory=FileChatMessageHistory("memory/ollama_session.json")
)

def main():
    parser = argparse.ArgumentParser(description="Delegent CLI Agent")
    parser.add_argument("query", nargs="+", help="The query or command to run")
    parser.add_argument("--llm", choices=["ollama_local","ollama", "gemini"], default="gemini", help="LLM backend to use")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    query = " ".join(args.query)

    if args.llm == "ollama":
        ollama = True
    else:
        ollama = False

    if args.llm == "ollama_local":
        ollama_local = True
    else:
        ollama_local = False

    agent = DelegentConversationalAgent(
        memory=memory,
        structured_tools=all_tools.tools,  
        ollama=ollama,
        ollama_local=ollama_local,
        verbose=args.verbose
    )

    response = agent.run(query)
    print("\nAgent Response:\n", response)


if __name__ == "__main__":
    main()
