from app.llm import get_planner_llm
from app.prompts.planner import get_planner_prompt
from app.schema import PlannerDecision
from app.utils.planner_parser import PlannerParser
from app.configurations.runtime import runtime_manager


def invoke_planner(messages) -> PlannerDecision:

    llm = get_planner_llm()

    prompt = get_planner_prompt()

    runtime = runtime_manager.runtime

    if runtime.provider.name in {
        "openrouter",
        "google",
    }:

        chain = (
            prompt
            | llm.with_structured_output(
                PlannerDecision
            )
        )

        try:
            return chain.invoke(
                {
                    "messages": messages
                }
            )
        except Exception:
            pass

    chain = (
        prompt
        | llm
    )

    response = chain.invoke(
        {
            "messages": messages
        }
    )

    return PlannerParser.parse_or_fallback(
        response.content
    )
