from app.llm_manager import llm_manager


def get_chat_llm():

    return llm_manager.get_llm(
        role="chat"
    )


def get_planner_llm():

    return llm_manager.get_llm(
        role="planner"
    )