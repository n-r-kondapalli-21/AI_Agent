from app.llm import get_chat_llm
from app.prompts.chat import chat_prompt


def get_chat_chain():
    """
    Build a chat chain using the currently
    active LLM.
    """

    llm = get_chat_llm()

    return (chat_prompt | llm)   