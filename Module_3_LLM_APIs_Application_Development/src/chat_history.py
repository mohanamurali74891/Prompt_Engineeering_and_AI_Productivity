"""
Module 3: LLM APIs & Application Development
=============================================
chat_history.py — Conversation history manager

Manages multi-turn conversation state including system instructions,
user/assistant messages, history trimming, and export/import.
"""

import json
import time
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field, asdict
from copy import deepcopy


# ─────────────────────────────────────────────────────────────
# ChatMessage (re-exported for convenience)
# ─────────────────────────────────────────────────────────────

@dataclass
class ChatMessage:
    """A single message in a conversation."""
    role: str                    # "system", "user", or "assistant"
    content: str
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, str]:
        """Return a minimal dict for passing to LLM APIs."""
        return {"role": self.role, "content": self.content}

    def __repr__(self):
        preview = self.content[:60].replace("\n", " ")
        return f"ChatMessage(role={self.role!r}, content={preview!r}...)"


# ─────────────────────────────────────────────────────────────
# ChatHistory
# ─────────────────────────────────────────────────────────────

class ChatHistory:
    """
    Manages a multi-turn conversation history.

    Features
    --------
    - Stores system, user, and assistant messages
    - Automatic trimming to stay within a token/message budget
    - Export to / import from JSON
    - Simple summary statistics

    Example
    -------
    >>> history = ChatHistory(system_prompt="You are a helpful assistant.")
    >>> history.add_user("Hello!")
    >>> history.add_assistant("Hi! How can I help you?")
    >>> messages = history.get_messages()   # pass to LLM client
    """

    def __init__(
        self,
        system_prompt: Optional[str] = None,
        max_messages: int = 20,
    ):
        """
        Parameters
        ----------
        system_prompt : str, optional
            Sets the AI's behaviour for the entire conversation.
        max_messages : int
            Maximum number of *non-system* messages to keep.
            Oldest messages are dropped when this limit is exceeded.
            Default is 20 (10 turns).
        """
        self._system_prompt = system_prompt
        self.max_messages = max_messages
        self._history: List[ChatMessage] = []

    # ── System prompt ────────────────────────────────────────

    @property
    def system_prompt(self) -> Optional[str]:
        return self._system_prompt

    @system_prompt.setter
    def system_prompt(self, value: str):
        self._system_prompt = value

    # ── Adding messages ──────────────────────────────────────

    def add_user(self, content: str, **metadata) -> ChatMessage:
        """Append a user message to the history."""
        msg = ChatMessage(role="user", content=content, metadata=metadata)
        self._history.append(msg)
        self._trim()
        return msg

    def add_assistant(self, content: str, **metadata) -> ChatMessage:
        """Append an assistant (model) message to the history."""
        msg = ChatMessage(role="assistant", content=content, metadata=metadata)
        self._history.append(msg)
        return msg

    def add_message(self, role: str, content: str, **metadata) -> ChatMessage:
        """Generic method to add any message role."""
        if role not in ("system", "user", "assistant"):
            raise ValueError(f"Invalid role: {role!r}. Use 'system', 'user', or 'assistant'.")
        msg = ChatMessage(role=role, content=content, metadata=metadata)
        if role != "system":
            self._history.append(msg)
            self._trim()
        else:
            self._system_prompt = content
        return msg

    # ── Retrieval ─────────────────────────────────────────────

    def get_messages(self) -> List[ChatMessage]:
        """
        Return the full message list, prepending the system prompt if set.
        This is the list you pass to your LLM client.
        """
        messages = []
        if self._system_prompt:
            messages.append(ChatMessage(role="system", content=self._system_prompt))
        messages.extend(self._history)
        return messages

    def get_messages_as_dicts(self) -> List[Dict[str, str]]:
        """Return messages as plain dicts — compatible with OpenAI/Gemini APIs."""
        return [m.to_dict() for m in self.get_messages()]

    def last_user_message(self) -> Optional[str]:
        """Return the content of the most recent user message."""
        for msg in reversed(self._history):
            if msg.role == "user":
                return msg.content
        return None

    def last_assistant_message(self) -> Optional[str]:
        """Return the content of the most recent assistant message."""
        for msg in reversed(self._history):
            if msg.role == "assistant":
                return msg.content
        return None

    # ── History management ────────────────────────────────────

    def clear(self):
        """Clear all messages (system prompt is preserved)."""
        self._history.clear()

    def reset(self, system_prompt: Optional[str] = None):
        """Clear all messages and optionally reset the system prompt."""
        self._history.clear()
        if system_prompt is not None:
            self._system_prompt = system_prompt

    def _trim(self):
        """Drop oldest messages when max_messages is exceeded."""
        if len(self._history) > self.max_messages:
            excess = len(self._history) - self.max_messages
            self._history = self._history[excess:]

    # ── Stats ─────────────────────────────────────────────────

    @property
    def turn_count(self) -> int:
        """Number of complete user/assistant exchange pairs."""
        user_count = sum(1 for m in self._history if m.role == "user")
        return user_count

    @property
    def total_characters(self) -> int:
        """Approximate character count of the entire history."""
        total = len(self._system_prompt or "")
        total += sum(len(m.content) for m in self._history)
        return total

    def summary(self) -> str:
        """Return a human-readable summary of the history state."""
        return (
            f"ChatHistory | "
            f"Turns: {self.turn_count} | "
            f"Messages: {len(self._history)} | "
            f"Chars: {self.total_characters:,} | "
            f"System prompt: {'✅' if self._system_prompt else '❌'}"
        )

    # ── Serialisation ─────────────────────────────────────────

    def to_json(self, indent: int = 2) -> str:
        """Serialise the conversation to a JSON string."""
        data = {
            "system_prompt": self._system_prompt,
            "max_messages": self.max_messages,
            "messages": [
                {
                    "role": m.role,
                    "content": m.content,
                    "timestamp": m.timestamp,
                    "metadata": m.metadata,
                }
                for m in self._history
            ],
        }
        return json.dumps(data, indent=indent, ensure_ascii=False)

    def save(self, filepath: str):
        """Save conversation to a JSON file."""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.to_json())
        print(f"💾 Conversation saved to: {filepath}")

    @classmethod
    def load(cls, filepath: str) -> "ChatHistory":
        """Load a conversation from a JSON file."""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        history = cls(
            system_prompt=data.get("system_prompt"),
            max_messages=data.get("max_messages", 20),
        )
        for m in data.get("messages", []):
            msg = ChatMessage(
                role=m["role"],
                content=m["content"],
                timestamp=m.get("timestamp", time.time()),
                metadata=m.get("metadata", {}),
            )
            history._history.append(msg)
        print(f"📂 Conversation loaded from: {filepath}")
        return history

    def __len__(self) -> int:
        return len(self._history)

    def __repr__(self) -> str:
        return self.summary()


# ─────────────────────────────────────────────────────────────
# Quick demo
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    history = ChatHistory(
        system_prompt="You are a knowledgeable AI assistant specialised in Python.",
        max_messages=10,
    )

    history.add_user("What is a list comprehension?")
    history.add_assistant("A list comprehension is a concise way to create lists in Python.")
    history.add_user("Can you give me an example?")
    history.add_assistant("Sure! [x**2 for x in range(10)] gives [0, 1, 4, 9, ..., 81].")

    print(history)
    print(f"\n📨 Total messages (including system): {len(history.get_messages())}")
    print(f"🔄 Turns: {history.turn_count}")

    # Show all messages
    print("\n📜 Conversation:")
    for msg in history.get_messages():
        print(f"  [{msg.role.upper():10}] {msg.content[:80]}")
