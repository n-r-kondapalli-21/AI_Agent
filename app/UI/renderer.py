from rich.markdown import Markdown
from rich.rule import Rule
from rich.syntax import Syntax

from app.UI.console import console
from app.configurations.constants import AGENT_NAME


class Renderer:
    """
    Renders all assistant responses.
    """

    @staticmethod
    def response(content: str) -> None:
        """
        Display an AI response.
        """

        console.print()

        console.print(
            f"[agent]🤖 {AGENT_NAME}[/agent]"
        )

        console.print()

        # Detect fenced code blocks
        if "```" in content:

            Renderer._markdown(content)

        else:

            console.print(content)

        console.print()

        console.print(
            Rule(style="muted")
        )

        console.print()

    @staticmethod
    def _markdown(content: str):

        console.print(
            Markdown(
                content,
                code_theme="dracula",
            )
        )

    @staticmethod
    def code(code: str, language: str = "python"):

        console.print(
            Syntax(
                code,
                language,
                theme="dracula",
                line_numbers=False,
                word_wrap=True,
            )
        )