from rich.panel import Panel
from rich.align import Align

from app.UI.console import console

from app.configurations.constants import (
    AGENT_NAME,
    FRAMEWORK_NAME,
    VERSION,
)


def show_banner() -> None:
    """
    Display application banner.
    """

    console.print()

    console.print(
        Panel(
            Align.center(
                f"""
🤖 {FRAMEWORK_NAME}

Version : {VERSION}

Agent : {AGENT_NAME}
"""
            ),
            title="Welcome",
            border_style="info",
            expand=False,
        )
    )

    console.print(
        "[muted]Type '/settings' for configuration.[/muted]"
    )

    console.print(
        "[muted]Type 'exit' or 'quit' to stop.[/muted]"
    )

    console.print()