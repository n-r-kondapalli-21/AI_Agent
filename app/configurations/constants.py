AGENT_NAME = "Hasini"

FRAMEWORK_NAME = "My AI Agent Framework"

VERSION = "1.0.0"

# ======================================================
# LLM Settings
# ======================================================

PLANNER_MAX_TOKENS = 1000

CHAT_MAX_TOKENS = 5000

# ======================================================
# Model Preferences by Provider
# ======================================================

# OpenRouter
OPENROUTER_PLANNER_MODEL = "nvidia/nemotron-3-super-120b-a12b:free"
OPENROUTER_CHAT_MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"

# Google AI Studio
GOOGLE_PLANNER_MODEL = "gemini-2.5-flash-lite"
GOOGLE_CHAT_MODEL = "gemini-2.5-pro"

# Z.ai
ZAI_PLANNER_MODEL = "glm-4.5-flash"
ZAI_CHAT_MODEL = "glm-4.7-flash"

# Ollama
OLLAMA_PLANNER_MODEL = "phi4-mini"
OLLAMA_CHAT_MODEL = "qwen3:4b"

# ======================================================
# File System Tool
# ======================================================

FILESYSTEM_ALLOWED_DRIVE = "D:"