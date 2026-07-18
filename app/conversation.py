from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    BaseMessage
)


class ConversationManager:
    """
    Manages conversation history for the current session.
    """

    def __init__(self):
        self._messages: list[BaseMessage] = []

    def add_user_message(self, content: str) -> None:
        """
        Add a user message.
        """
        self._messages.append(
            HumanMessage(content=content)
        )

    def add_ai_message(self, message: AIMessage) -> None:
        """
        Add an AI response.
        """
        self._messages.append(message)

    def get_messages(self) -> list[BaseMessage]:
        """
        Return all messages.
        """
        return self._messages.copy()

    def clear(self) -> None:
        """
        Clear conversation history.
        """
        self._messages.clear()

    def message_count(self) -> int:
        """
        Number of stored messages.
        """
        return len(self._messages)