from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class Provider:
    """
    Represents an LLM provider.
    """

    name: str

    display_name: str

    base_url: str

    api_key: Optional[str]

    models: list[str]


# ==========================================================
# OpenRouter
# ==========================================================

OPENROUTER = Provider(

    name="openrouter",

    display_name="OpenRouter",

    base_url="https://openrouter.ai/api/v1",

    api_key=None,

    models=[

        "poolside/laguna-m.1:free",

        "nvidia/nemotron-3-super-120b-a12b:free",

        "nvidia/nemotron-3-ultra-550b-a55b:free",

    ],

)

# ==========================================================
# Google AI Studio
# ==========================================================

GOOGLE_AI_STUDIO = Provider(

    name="google",

    display_name="Google AI Studio",

    base_url="https://generativelanguage.googleapis.com/v1beta",

    api_key=None,

    models=[

        "gemini-2.5-flash",

        "gemini-2.5-flash-lite",

        "gemini-2.5-pro",

        "gemini-flash-latest",

        "gemini-flash-lite-latest",

        "gemini-3.1-flash-lite",

        "gemini-3.1-pro-preview",

        "gemini-3-pro-preview",

        "gemini-3-flash-preview",

        "gemini-3.1-flash-lite-preview",

    ],

)

# ==========================================================
# Z.ai
# ==========================================================

Z_AI = Provider(

    name="zai",

    display_name="Z.ai",

    base_url="https://api.z.ai/api/paas/v4",

    api_key=None,

    models=[

        "glm-4.7-flash",

        "glm-4.5-flash",

    ],

)

# ==========================================================
# Ollama
# ==========================================================

OLLAMA = Provider(

    name="ollama",

    display_name="Ollama",

    base_url="http://localhost:11434/v1",

    api_key=None,

    models=[

        "qwen3:4b",

        "phi4-mini",

    ],

)

# ==========================================================
# Provider Registry
# ==========================================================

PROVIDERS = {

    OPENROUTER.name: OPENROUTER,

    GOOGLE_AI_STUDIO.name: GOOGLE_AI_STUDIO,

    Z_AI.name: Z_AI,

    OLLAMA.name: OLLAMA,

}