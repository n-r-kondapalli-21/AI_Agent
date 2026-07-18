from app.configurations.providers import PROVIDERS
from app.configurations.runtime import runtime_manager
from app.configurations.constants import (
    OPENROUTER_PLANNER_MODEL,
    OPENROUTER_CHAT_MODEL,
    GOOGLE_PLANNER_MODEL,
    GOOGLE_CHAT_MODEL,
    ZAI_PLANNER_MODEL,
    ZAI_CHAT_MODEL,
    OLLAMA_PLANNER_MODEL,
    OLLAMA_CHAT_MODEL,
)
from app.llm_manager import llm_manager


class RuntimeSelector:
    """
    Handles interactive runtime selection.
    """

    def _get_models_for_provider(self, provider_name: str) -> tuple:
        """Get planner and chat models for a provider."""
        model_mapping = {
            "openrouter": (OPENROUTER_PLANNER_MODEL, OPENROUTER_CHAT_MODEL),
            "google": (GOOGLE_PLANNER_MODEL, GOOGLE_CHAT_MODEL),
            "zai": (ZAI_PLANNER_MODEL, ZAI_CHAT_MODEL),
            "ollama": (OLLAMA_PLANNER_MODEL, OLLAMA_CHAT_MODEL),
        }
        return model_mapping.get(provider_name, (None, None))

    # ======================================================
    # Provider Selection
    # ======================================================

    def select_provider(self) -> None:

        providers = list(PROVIDERS.values())

        print("=" * 60)
        print("Available Providers")
        print("=" * 60)

        for index, provider in enumerate(
            providers,
            start=1
        ):

            print(
                f"{index}. {provider.display_name}"
            )

        while True:

            try:

                choice = input("\nSelect Provider (or 'exit' to cancel) : ").strip()

                if choice.lower() == 'exit':
                    print("\nCancelled.")
                    return

                choice = int(choice)

                if 1 <= choice <= len(providers):

                    provider = providers[
                        choice - 1
                    ]

                    runtime_manager.set_provider(
                        provider
                    )

                    planner_model, chat_model = self._get_models_for_provider(provider.name)

                    print(
                        f"\n✓ Active Provider : {provider.display_name}"
                    )

                    print(
                        f"✓ Planner Model   : {planner_model}"
                    )

                    print(
                        f"✓ Chat Model      : {chat_model}"
                    )

                    # Preload models for the new provider
                    print("\nPreloading models...")
                    llm_manager.get_llm(role="planner")
                    llm_manager.get_llm(role="chat")
                    print("Models loaded successfully.")

                    return

            except ValueError:
                pass

            except KeyboardInterrupt:
                print("\n\nCancelled.")
                return

            print("Invalid selection.")

    # ======================================================
    # Model Selection
    # ======================================================

    def select_model(self) -> None:

        provider = runtime_manager.runtime.provider

        print("=" * 60)
        print(
            f"Models ({provider.display_name})"
        )
        print("=" * 60)

        for index, model in enumerate(
            provider.models,
            start=1
        ):

            print(f"{index}. {model}")

        while True:

            try:

                choice = input("\nSelect Model (or 'exit' to cancel) : ").strip()

                if choice.lower() == 'exit':
                    print("\nCancelled.")
                    return

                choice = int(choice)

                if 1 <= choice <= len(provider.models):

                    model = provider.models[
                        choice - 1
                    ]

                    runtime_manager.set_model(
                        model
                    )

                    print(
                        f"\n✓ Active Model : {model}"
                    )

                    # Preload models after model change
                    print("\nPreloading models...")
                    llm_manager.get_llm(role="planner")
                    llm_manager.get_llm(role="chat")
                    print("Models loaded successfully.")

                    return

            except ValueError:
                pass

            except KeyboardInterrupt:
                print("\n\nCancelled.")
                return

            print("Invalid selection.")

    # ======================================================
    # Show Runtime Configuration
    # ======================================================

    def show_current(self) -> None:

        runtime = runtime_manager.runtime

        planner_model, chat_model = self._get_models_for_provider(runtime.provider.name)

        print("\n" + "=" * 60)
        print("Current Runtime Configuration")
        print("=" * 60)

        print(
            f"Provider       : {runtime.provider.display_name}"
        )

        print(
            f"Planner Model  : {planner_model}"
        )

        print(
            f"Chat Model     : {chat_model}"
        )

        print(
            f"Base URL       : {runtime.provider.base_url}"
        )

        print(
            f"Temperature    : {runtime.temperature}"
        )

        print(
            f"Max Tokens     : {runtime.max_tokens}"
        )

        print("=" * 60)