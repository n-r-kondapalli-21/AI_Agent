from dataclasses import dataclass

from app.configurations.config import settings
from app.configurations.providers import (Provider,PROVIDERS,)



@dataclass(slots=True)
class RuntimeConfig:
    """
    Represents the currently active LLM configuration.
    """

    provider: Provider

    model: str

    temperature: float

    max_tokens: int


class RuntimeManager:
    """
    Manages the active runtime configuration.
    """

    def __init__(self):

        default_provider = PROVIDERS.get(
            settings.default_provider,
            next(iter(PROVIDERS.values()))
        )

        default_model = settings.default_model

        if (
            default_model is None
            or default_model not in default_provider.models
        ):
            default_model = default_provider.models[0]

        self._runtime = RuntimeConfig(

            provider=default_provider,

            model=default_model,

            temperature=settings.temperature,

            max_tokens=settings.max_tokens,

        )

    @property
    def runtime(self) -> RuntimeConfig:
        """
        Return the active runtime configuration.
        """

        return self._runtime

    def set_provider(self,provider: Provider) -> None:

        from app.llm_manager import llm_manager

        # No change
        if self._runtime.provider.name == provider.name:
            return

        self._runtime.provider = provider

        # Automatically switch to a compatible model
        if self._runtime.model not in provider.models:
            self._runtime.model = provider.models[0]

        llm_manager.clear_cache()

    def set_model(self,model: str) -> None:

        from app.llm_manager import llm_manager

        if model not in self._runtime.provider.models:
            raise ValueError(
                f"Model '{model}' is not available "
                f"for provider '{self._runtime.provider.display_name}'."
            )

        # No change
        if self._runtime.model == model:
            return

        self._runtime.model = model

        llm_manager.clear_cache()

    def set_temperature(
        self,
        temperature: float
    ) -> None:

        self._runtime.temperature = temperature

    def set_max_tokens(
        self,
        max_tokens: int
    ) -> None:

        self._runtime.max_tokens = max_tokens

    def get_current_provider(self) -> Provider:

        return self._runtime.provider

    def get_current_model(self) -> str:

        return self._runtime.model

    def show(self) -> None:

        print("\nCurrent Runtime Configuration")
        print("-" * 40)
        print(f"Provider    : {self._runtime.provider.display_name}")
        print(f"Model       : {self._runtime.model}")
        print(f"Base URL    : {self._runtime.provider.base_url}")
        print(f"Temperature : {self._runtime.temperature}")
        print(f"Max Tokens  : {self._runtime.max_tokens}")
        print("-" * 40)


runtime_manager = RuntimeManager()