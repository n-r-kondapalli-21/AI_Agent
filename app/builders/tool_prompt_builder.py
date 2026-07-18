from app.tools.registry import tool_registry


class ToolPromptBuilder:
    """
    Builds the tool descriptions used by the planner.
    """

    @staticmethod
    def build() -> str:

        sections = []

        for tool in tool_registry.list_tools():

            metadata = tool.metadata

            usage = "\n".join(
                f"- {item}"
                for item in metadata.usage
            )

            parameters = "\n".join(
                f"- {key}: {value}"
                for key, value in metadata.parameters.items()
            )

            examples = "\n".join(
                f"- {item}"
                for item in metadata.examples
            )

            section = f"""
Tool: {tool.name.value}

Description:
{metadata.description}

Use When:
{usage}

Parameters:
{parameters}

Examples:
{examples}
"""

            sections.append(
                section.strip()
            )

        return "\n\n".join(sections)