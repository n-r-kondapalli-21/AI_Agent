from langchain_openai import ChatOpenAI

from app.configurations.constants import (
    CHAT_MAX_TOKENS,
    PLANNER_MAX_TOKENS,
    OPENROUTER_PLANNER_MODEL,
    OPENROUTER_CHAT_MODEL,
    GOOGLE_PLANNER_MODEL,
    GOOGLE_CHAT_MODEL,
    ZAI_PLANNER_MODEL,
    ZAI_CHAT_MODEL,
    OLLAMA_PLANNER_MODEL,
    OLLAMA_CHAT_MODEL,
)

from app.configurations.runtime import runtime_manager


class LLMManager:
    """
    Creates and caches LLM instances for different roles.
    """

    def __init__(self):

        self._cache = {}

    def _get_model_for_role(
        self,
        role: str,
        provider_name: str
    ) -> str:
        """
        Get the appropriate model for a given role and provider.
        """
        model_mapping = {
            "openrouter": {
                "planner": OPENROUTER_PLANNER_MODEL,
                "chat": OPENROUTER_CHAT_MODEL,
            },
            "google": {
                "planner": GOOGLE_PLANNER_MODEL,
                "chat": GOOGLE_CHAT_MODEL,
            },
            "zai": {
                "planner": ZAI_PLANNER_MODEL,
                "chat": ZAI_CHAT_MODEL,
            },
            "ollama": {
                "planner": OLLAMA_PLANNER_MODEL,
                "chat": OLLAMA_CHAT_MODEL,
            },
        }

        # For chat role, always use the dedicated chat model from constants
        # unless the runtime model is explicitly different from the default planner model
        if role == "chat":
            provider_models = model_mapping.get(provider_name, {})
            default_chat_model = provider_models.get("chat")
            default_planner_model = provider_models.get("planner")
            # Only use runtime model if it's different from both default models
            if (default_chat_model and 
                runtime_manager.runtime.model != default_chat_model and 
                runtime_manager.runtime.model != default_planner_model):
                return runtime_manager.runtime.model

        return model_mapping.get(
            provider_name,
            {}
        ).get(role, runtime_manager.runtime.model)

    def get_llm(
        self,
        role: str = "chat",
    ):

        runtime = runtime_manager.runtime

        if role == "planner":

            max_tokens = PLANNER_MAX_TOKENS
            model = self._get_model_for_role(role, runtime.provider.name)

        else:

            max_tokens = CHAT_MAX_TOKENS
            model = self._get_model_for_role(role, runtime.provider.name)

        cache_key = (
            runtime.provider.name,
            model,
            role,
        )

        if cache_key not in self._cache:

            llm = ChatOpenAI(

                model=model,

                api_key=runtime.provider.api_key,

                base_url=runtime.provider.base_url,

                temperature=runtime.temperature,

                max_tokens=max_tokens,

            )

            self._cache[cache_key] = llm

            print(
                f"\n✓ Loaded {runtime.provider.display_name}"
            )

            print(
                f"✓ Model : {model}"
            )

            print(
                f"✓ Role  : {role}\n"
            )

        return self._cache[cache_key]

    def clear_cache(self):

        """
        Clears all cached LLM instances.
        """

        self._cache.clear()


llm_manager = LLMManager()