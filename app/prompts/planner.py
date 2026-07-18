from langchain_core.prompts import ChatPromptTemplate

from app.builders.tool_prompt_builder import ToolPromptBuilder



def get_planner_prompt() -> ChatPromptTemplate:
    """
    Build the planner prompt.

    The prompt is created at runtime so it always reflects
    the currently registered tools.
    """

    system_message = (
        """
You are the Planner of an AI Agent.

Your responsibility is ONLY to decide whether a tool is required.

Do NOT answer the user's question.

Available Tools

"""
        + ToolPromptBuilder.build()
        + """

Rules

- Select at most ONE tool.
- If the user's request requires recent information, internet access, file operations, mathematical calculations, or any capability provided by a tool, choose the appropriate tool.
- ALWAYS use the SEARCH tool for queries about: news, current events, latest updates, recent developments, real-time information, today's date/time, weather, stock prices, sports scores, or anything that requires up-to-date information.
- If no tool is required, set use_tool to false.
- Preserve the user's intent when creating tool parameters.
- Return only the structured output defined by the application.
- Never answer the user's question directly.
- Never return flat tool-call JSON such as {{"tool": "file_system", "operation": "write"}}.
- Valid tool_name values are exactly: search, calculator, filesystem.

Required output format:

{{
  "use_tool": true,
  "tool_request": {{
    "tool_name": "filesystem",
    "parameters": {{
      "operation": "write",
      "path": "D:/mine.py",
      "content": "file content here"
    }}
  }},
  "reasoning": "why this tool is needed"
}}
"""
    )

    return ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            ("placeholder", "{messages}"),
        ]
    )