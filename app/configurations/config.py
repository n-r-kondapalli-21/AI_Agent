import os

from dataclasses import dataclass

from dotenv import load_dotenv

from app.configurations.providers import PROVIDERS


# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()


# ==========================================================
# Runtime Defaults
# ==========================================================

@dataclass(slots=True)
class Settings:
    """
    Global application settings.
    """

    temperature: float

    max_tokens: int

    default_provider: str | None

    default_model: str | None


# ==========================================================
# API Keys
# ==========================================================

_PROVIDER_API_KEYS = {

    "openrouter": os.getenv("OPENROUTER_API_KEY"),

    "google": os.getenv("GOOGLE_API_KEY"),

    "zai": os.getenv("ZAI_API_KEY"),

    "ollama": None,

}


# ==========================================================
# Inject API Keys into Providers
# ==========================================================

for provider in PROVIDERS.values():

    provider.api_key = _PROVIDER_API_KEYS.get(
        provider.name
    )


# ==========================================================
# Global Settings
# ==========================================================

settings = Settings(

    temperature=float(
        os.getenv(
            "TEMPERATURE",
            "0"
        )
    ),

    max_tokens=int(
        os.getenv(
            "MAX_TOKENS",
            "2000"
        )
    ),

    default_provider=os.getenv(
        "DEFAULT_PROVIDER"
    ),

    default_model=os.getenv(
        "DEFAULT_MODEL"
    )

)