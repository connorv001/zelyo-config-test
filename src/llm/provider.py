"""LLM Provider abstraction for multi-provider support."""

import os
from typing import Optional
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage


def get_llm_provider() -> BaseChatModel:
    """
    Get LLM provider based on environment configuration.
    
    Supports: openai, gemini, openrouter
    """
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    
    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.1,
        )
    
    elif provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.1,
        )
    
    elif provider == "openrouter":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet"),
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
            temperature=0.1,
            default_headers={
                "HTTP-Referer": os.getenv("OPENROUTER_REFERER", "https://zelyo.io"),
                "X-Title": "Zelyo Config Guardian",
            }
        )
    
    else:
        raise ValueError(f"Unknown LLM provider: {provider}. Supported: openai, gemini, openrouter")


class LLMClient:
    """Unified LLM client for Zelyo."""
    
    def __init__(self):
        self.llm = get_llm_provider()
    
    async def invoke(self, system_prompt: str, user_prompt: str) -> str:
        """Invoke LLM with system and user prompts."""
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
        response = await self.llm.ainvoke(messages)
        return response.content
    
    def invoke_sync(self, system_prompt: str, user_prompt: str) -> str:
        """Synchronous invoke for simpler use cases."""
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
        response = self.llm.invoke(messages)
        return response.content
