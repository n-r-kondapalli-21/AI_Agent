from contextlib import contextmanager

from app.UI.console import console

from app.configurations.constants import AGENT_NAME


@contextmanager
def thinking(message: str = "Thinking..."):
    """
    Display a spinner while the agent is working.
    """

    with console.status(
        f"[info]{AGENT_NAME} • {message}[/info]"
    ):
        yield