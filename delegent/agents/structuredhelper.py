# structuredhelper.py

import warnings
warnings.filterwarnings("ignore")

from typing import List, Optional
from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from langchain.tools.base import BaseTool
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.tools import Tool

from langchain_google_genai import ChatGoogleGenerativeAI
from delegent.llms import RemoteOllamaLLM


class StructuredToolAgent:
    """
    A structured conversational agent using LangChain with user-defined tools and LLMs.
    Defaults to Gemini if no LLM is provided.
    """

    def __init__(
        self,
        tools: List,
        llm: Optional[BaseChatModel] = None,
        verbose: bool = False
    ):
        """
        Initialize the agent with user-defined tools and an optional custom LLM.

        Args:
            tools (List[BaseTool]): List of LangChain-compatible tools.
            llm (BaseChatModel, optional): Custom chat-compatible LLM. Defaults to Gemini.
            verbose (bool): Whether to enable verbose output for debugging.
        """
        self.tools = tools
        self.llm = llm or self._default_llm()
        self.agent = self._initialize_agent(verbose=verbose)

    def _default_llm(self) -> BaseChatModel:
        """Load and return the default Gemini model."""
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-lite",
            temperature=0.7
        )

        # To use Ollama by default instead, comment the above and uncomment below:
        # return RemoteOllamaLLM()

    def _initialize_agent(self, verbose: bool = False):
        """Create the structured chat agent."""
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=verbose
        )

    def run(self, query: str) -> str:
        """
        Execute a query through the agent.

        Args:
            query (str): User's input question or command.

        Returns:
            str: Agent's response.
        """
        return self.agent.run(query)
