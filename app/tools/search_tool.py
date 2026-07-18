from ddgs import DDGS

from app.enums import ToolName

from app.schema import (
    SearchItem,
    SearchResult,
    ToolMetadata,
    ToolResult,
)

from app.tools.base import BaseTool


class DuckDuckGoSearchTool(BaseTool):
    """
    Search the web using DuckDuckGo.
    """

    def __init__(self):

        super().__init__(
            name=ToolName.SEARCH,

            metadata=ToolMetadata(

                description="Search the web for recent and real-time information.",

                usage=[
                    "Latest news",
                    "Current events",
                    "Real-time information",
                    "Internet search",
                    "Stock market updates",
                    "Sports results",
                    "Recent technology updates",
                    "Live information"
                ],

                parameters={
                    "query": "search query",
                    "max_results": 5
                },

                examples=[
                    "Latest AI news",
                    "NVIDIA latest news",
                    "Weather in Hyderabad",
                    "India stock market today"
                ]
            )
        )

    def run(
        self,
        query: str,
        max_results: int = 5
    ) -> ToolResult:

        try:

            with DDGS() as ddgs:

                raw_results = list(
                    ddgs.text(
                        query=query,
                        max_results=max_results
                    )
                )

            search_items = []

            for item in raw_results:

                search_items.append(

                    SearchItem(

                        title=item.get(
                            "title",
                            ""
                        ),

                        url=item.get(
                            "href",
                            ""
                        ),

                        snippet=item.get(
                            "body",
                            ""
                        )

                    )

                )

            search_result = SearchResult(

                query=query,

                results=search_items

            )

            return ToolResult(

                success=True,

                tool_name=self.name,

                content=search_result

            )

        except Exception as e:

            return ToolResult(

                success=False,

                tool_name=self.name,

                content=None,

                error=str(e)

            )

    def format_for_prompt(
        self,
        result: ToolResult
    ) -> str:

        if (
            not result.success
            or result.content is None
        ):
            return ""

        search_result: SearchResult = result.content

        lines = [

            f"Search Query: {search_result.query}",

            "",

            "Search Results:",

            ""

        ]

        for index, item in enumerate(

            search_result.results,

            start=1

        ):

            lines.extend(

                [

                    f"[{index}] {item.title}",

                    f"URL: {item.url}",

                    f"Snippet: {item.snippet}",

                    ""

                ]

            )

        return "\n".join(lines)