# central.py

import warnings
warnings.filterwarnings("ignore")

from typing import List, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import initialize_agent
from langchain_classic.agents.agent_types import AgentType
from langchain_classic.tools import Tool
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.base_memory import BaseMemory

import os 
from dotenv import load_dotenv
load_dotenv()

from delegent.agents.structuredhelper import StructuredToolAgent
from delegent.llms import RemoteOllamaLLM
from delegent.llms import LocalOllamaLLM

memory_inbuilt = ConversationBufferMemory(memory_key="chat_history",return_messages=True)

class DelegentConversationalAgent:
    """
    A conversational agent using Gemini, with access to a structured helper agent.
    The structured agent is used as a fallback tool when the main agent cannot handle a query.
    """

    def __init__(
        self,
        structured_tools: List,
        memory: Optional[BaseMemory] = None,
        structured_llm: Optional[BaseChatModel] = None,
        main_llm: Optional[BaseChatModel] = None,
        ollama: bool = False,
        ollama_local: bool = False,
        verbose: bool = False
    ):
        """
        Initializes the main agent with the structured agent as a helper tool.

        Args:
            structured_tools (List[BaseTool]): Tools to be passed into the StructuredToolAgent.
            structured_llm (BaseChatModel, optional): LLM for the StructuredToolAgent.
            main_llm (BaseChatModel, optional): LLM for this conversational agent. Defaults to Gemini.
            verbose (bool): Enable verbose output.
        """

        self.ollama = ollama
        self.ollama_local = ollama_local

        self.memory = memory or memory_inbuilt
        
        # Step 2: Load main conversational LLM
        self.llm = main_llm or self._default_main_llm()

        self.structured_llm =structured_llm or main_llm or self._default_main_llm()

        # Step 1: Create structured agent with user-defined tools and llm
        self.structured_agent = StructuredToolAgent(
            tools=structured_tools,
            llm=structured_llm,
            verbose=verbose
        )

        

        # Step 3: Wrap structured agent as a tool
        self.tools = self._load_tools()

        # Step 4: Initialize final agent
        self.agent = self._initialize_agent(verbose=verbose)

        

    def _default_main_llm(self) -> BaseChatModel:
        """Load Gemini as the default LLM."""
        if self.ollama:
            return RemoteOllamaLLM.RemoteOllamaLLM()
        if self.ollama_local:
            return LocalOllamaLLM.LocalOllamaLLM()
        else:
            return ChatGoogleGenerativeAI(
                model= os.getenv('GEMINI_MODEL'),
                temperature=0.7
            )

    def _load_tools(self) -> List[Tool]:
        """Return the structured agent as a Tool for fallback use."""
        return [
            Tool(
                name="Helper",
                func=self.structured_agent.run,
                description=(
                    "Use this tool if you can't answer the query yourself — for example, "
                    "if the query requires structured processing like math, web access, or external tools. "
                    "Pass the full user query as the input."
                )
            )
        ]

    def _initialize_agent(self, verbose: bool):
        """Initialize and return the main conversational agent."""
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory = self.memory,
            verbose=verbose
        )

    def run(self, query: str) -> str:
        """Execute a query through the main agent."""
        return self.agent.run(query)
