from rich.table import Table

from app.UI.console import console

from app.configurations.runtime import runtime_manager


def show_runtime_status() -> None:
    """
    Display current runtime configuration.
    """

    runtime = runtime_manager.runtime

    table = Table(
        title="Runtime Configuration",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Property")
    table.add_column("Value")

    table.add_row(
        "Provider",
        runtime.provider.display_name,
    )

    table.add_row(
        "Model",
        runtime.model,
    )

    table.add_row(
        "Temperature",
        str(runtime.temperature),
    )

    table.add_row(
        "Max Tokens",
        str(runtime.max_tokens),
    )

    console.print(table)