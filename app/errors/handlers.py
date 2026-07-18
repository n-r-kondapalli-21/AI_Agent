from rich.panel import Panel
from rich.text import Text
from rich.box import ROUNDED

from app.UI.console import console
from app.configurations.runtime import runtime_manager


class AgentError(Exception):
    """Base exception for agent errors."""
    pass


def handle_llm_error(error: Exception, debug: bool = False) -> None:
    """
    Handle LLM/API errors with user-friendly Rich panels.
    """
    runtime = runtime_manager.runtime
    error_msg = str(error).lower()
    
    # Determine error type and suggestions
    if "rate limit" in error_msg or "429" in error_msg:
        title = "⚠ Rate Limit Exceeded"
        suggestions = [
            "• Wait a few seconds",
            "• Switch provider (/provider)",
            "• Switch model (/model)",
        ]
    elif "timeout" in error_msg:
        title = "⏱ Request Timeout"
        suggestions = [
            "• Check your internet connection",
            "• Try again",
            "• Switch provider (/provider)",
        ]
    elif "connection" in error_msg:
        title = "🔌 Connection Error"
        suggestions = [
            "• Check your internet connection",
            "• Verify provider status",
            "• Switch provider (/provider)",
        ]
    elif "context length" in error_msg or "token" in error_msg:
        title = "📏 Context Length Exceeded"
        suggestions = [
            "• Clear conversation history",
            "• Use a model with larger context",
            "• Switch model (/model)",
        ]
    elif "api key" in error_msg or "authentication" in error_msg or "401" in error_msg:
        title = "🔑 Authentication Failed"
        suggestions = [
            "• Verify your API key",
            "• Check provider settings",
            "• Switch provider (/provider)",
        ]
    elif "model not found" in error_msg or "404" in error_msg:
        title = "🤖 Model Not Found"
        suggestions = [
            "• Verify model name",
            "• Switch model (/model)",
            "• Switch provider (/provider)",
        ]
    elif "overload" in error_msg or "503" in error_msg:
        title = "⚡ Provider Overloaded"
        suggestions = [
            "• Wait a moment",
            "• Switch provider (/provider)",
            "• Try again later",
        ]
    elif "tool" in error_msg:
        title = "🔧 Tool Execution Failed"
        suggestions = [
            "• Try a different approach",
            "• Rephrase your request",
            "• Check tool permissions",
        ]
    else:
        title = "❌ Unexpected Error"
        suggestions = [
            "• Try again",
            "• Switch provider (/provider)",
            "• Enable DEBUG mode for details",
        ]
    
    # Build error panel content
    content = Text()
    content.append(f"Provider : {runtime.provider.display_name}\n", style="provider")
    content.append(f"Model    : {runtime.model}\n", style="model")
    content.append("\nSuggestions:\n", style="bold")
    for suggestion in suggestions:
        content.append(f"{suggestion}\n", style="muted")
    
    console.print()
    console.print(
        Panel(
            content,
            title=f"[error]{title}[/error]",
            border_style="error",
            box=ROUNDED,
            padding=(1, 2),
        )
    )
    
    # Show traceback in DEBUG mode
    if debug:
        console.print()
        console.print_exception(show_locals=False)
