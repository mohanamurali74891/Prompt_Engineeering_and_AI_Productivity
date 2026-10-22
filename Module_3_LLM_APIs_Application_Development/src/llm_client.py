"""
Module 3: LLM APIs & Application Development
=============================================
llm_client.py — Core LLM API wrapper

Provides a unified interface for both Google Gemini and OpenAI APIs.
Handles authentication, request formatting, and response parsing.
"""

import os
import time
import logging
from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass, field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────
# Data Classes
# ─────────────────────────────────────────────────────────────

@dataclass
class LLMResponse:
    """Standardised response object returned by all LLM clients."""
    text: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    finish_reason: str = "stop"
    raw: Any = None                   # Raw SDK response for advanced use

    @property
    def token_summary(self) -> str:
        return (
            f"Prompt: {self.prompt_tokens} | "
            f"Completion: {self.completion_tokens} | "
            f"Total: {self.total_tokens}"
        )


@dataclass
class ChatMessage:
    """A single message in a conversation."""
    role: str          # "system", "user", or "assistant"
    content: str


# ─────────────────────────────────────────────────────────────
# Base Client
# ─────────────────────────────────────────────────────────────

class BaseLLMClient:
    """Abstract base class for LLM API clients."""

    def __init__(self, model: str, max_retries: int = 3, retry_delay: float = 2.0):
        self.model = model
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs,
    ) -> LLMResponse:
        """Send a list of messages and return an LLMResponse. Override in subclasses."""
        raise NotImplementedError

    def _retry(self, func, *args, **kwargs):
        """Retry wrapper with exponential back-off."""
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                wait = self.retry_delay * (2 ** (attempt - 1))
                logger.warning(f"Attempt {attempt} failed: {e}. Retrying in {wait:.1f}s...")
                time.sleep(wait)
        logger.error(f"All {self.max_retries} retries exhausted.")
        raise last_error


# ─────────────────────────────────────────────────────────────
# Google Gemini Client
# ─────────────────────────────────────────────────────────────

class GeminiClient(BaseLLMClient):
    """
    LLM client for Google Gemini API.

    Usage:
        client = GeminiClient()
        response = client.chat([ChatMessage("user", "Hello!")])
        print(response.text)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-1.5-flash",
        max_retries: int = 3,
        retry_delay: float = 2.0,
    ):
        super().__init__(model, max_retries, retry_delay)
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Set GEMINI_API_KEY in your .env file "
                "or pass api_key= to GeminiClient()."
            )
        self._configure()

    def _configure(self):
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self._genai = genai
            logger.info(f"✅ Gemini client configured (model: {self.model})")
        except ImportError:
            raise ImportError(
                "google-generativeai is not installed. "
                "Run: pip install google-generativeai"
            )

    def chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs,
    ) -> LLMResponse:
        """
        Send messages to Gemini and return a standardised LLMResponse.

        Parameters
        ----------
        messages : list of ChatMessage
            Conversation history including system, user, and assistant turns.
        temperature : float
            Controls randomness (0.0 = deterministic, 1.0 = very creative).
        max_tokens : int
            Maximum tokens in the generated response.
        """
        def _call():
            # Extract system instruction from messages
            system_instruction = None
            gemini_history = []

            for msg in messages:
                if msg.role == "system":
                    system_instruction = msg.content
                elif msg.role == "user":
                    gemini_history.append({"role": "user", "parts": [msg.content]})
                elif msg.role == "assistant":
                    gemini_history.append({"role": "model", "parts": [msg.content]})

            # Separate the last user message for generate_content
            last_user_message = None
            history_without_last = gemini_history

            if gemini_history and gemini_history[-1]["role"] == "user":
                last_user_message = gemini_history[-1]["parts"][0]
                history_without_last = gemini_history[:-1]

            model_kwargs = {"model_name": self.model}
            if system_instruction:
                model_kwargs["system_instruction"] = system_instruction

            model = self._genai.GenerativeModel(**model_kwargs)

            generation_config = self._genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )

            if history_without_last:
                chat_session = model.start_chat(history=history_without_last)
                raw = chat_session.send_message(
                    last_user_message or "",
                    generation_config=generation_config,
                )
            else:
                raw = model.generate_content(
                    last_user_message or "",
                    generation_config=generation_config,
                )

            usage = raw.usage_metadata
            return LLMResponse(
                text=raw.text,
                model=self.model,
                prompt_tokens=getattr(usage, "prompt_token_count", 0),
                completion_tokens=getattr(usage, "candidates_token_count", 0),
                total_tokens=getattr(usage, "total_token_count", 0),
                finish_reason=str(raw.candidates[0].finish_reason) if raw.candidates else "stop",
                raw=raw,
            )

        return self._retry(_call)

    def count_tokens(self, text: str) -> int:
        """Count tokens for a given text string using Gemini's token counter."""
        model = self._genai.GenerativeModel(self.model)
        result = model.count_tokens(text)
        return result.total_tokens


# ─────────────────────────────────────────────────────────────
# OpenAI Client
# ─────────────────────────────────────────────────────────────

class OpenAIClient(BaseLLMClient):
    """
    LLM client for OpenAI API.

    Usage:
        client = OpenAIClient()
        response = client.chat([ChatMessage("user", "Hello!")])
        print(response.text)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o-mini",
        max_retries: int = 3,
        retry_delay: float = 2.0,
    ):
        super().__init__(model, max_retries, retry_delay)
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY in your .env file "
                "or pass api_key= to OpenAIClient()."
            )
        self._configure()

    def _configure(self):
        try:
            from openai import OpenAI
            self._client = OpenAI(api_key=self.api_key)
            logger.info(f"✅ OpenAI client configured (model: {self.model})")
        except ImportError:
            raise ImportError("openai is not installed. Run: pip install openai")

    def chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs,
    ) -> LLMResponse:
        """
        Send messages to OpenAI and return a standardised LLMResponse.

        Parameters
        ----------
        messages : list of ChatMessage
        temperature : float
        max_tokens : int
        """
        def _call():
            formatted = [{"role": m.role, "content": m.content} for m in messages]
            raw = self._client.chat.completions.create(
                model=self.model,
                messages=formatted,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs,
            )
            choice = raw.choices[0]
            usage = raw.usage
            return LLMResponse(
                text=choice.message.content or "",
                model=raw.model,
                prompt_tokens=usage.prompt_tokens,
                completion_tokens=usage.completion_tokens,
                total_tokens=usage.total_tokens,
                finish_reason=choice.finish_reason,
                raw=raw,
            )

        return self._retry(_call)


# ─────────────────────────────────────────────────────────────
# Factory function
# ─────────────────────────────────────────────────────────────

def create_client(provider: str = "gemini", **kwargs) -> BaseLLMClient:
    """
    Factory function to create an LLM client by provider name.

    Parameters
    ----------
    provider : str
        "gemini" (default) or "openai"
    **kwargs
        Passed directly to the client constructor.

    Returns
    -------
    BaseLLMClient

    Example
    -------
    >>> client = create_client("gemini", model="gemini-1.5-pro")
    >>> response = client.chat([ChatMessage("user", "Hi!")])
    """
    providers = {
        "gemini": GeminiClient,
        "openai": OpenAIClient,
    }
    if provider not in providers:
        raise ValueError(f"Unknown provider '{provider}'. Choose from: {list(providers)}")
    return providers[provider](**kwargs)


# ─────────────────────────────────────────────────────────────
# Quick demo
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    client = create_client("gemini")
    messages = [
        ChatMessage("system", "You are a helpful AI assistant."),
        ChatMessage("user", "What is machine learning in one sentence?"),
    ]
    response = client.chat(messages, temperature=0.5, max_tokens=100)
    print(f"\n🤖 Response: {response.text}")
    print(f"📊 Tokens  : {response.token_summary}")
