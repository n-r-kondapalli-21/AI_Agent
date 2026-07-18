from sympy import sympify

from app.enums import ToolName

from app.schema import (
    CalculatorResult,
    ToolMetadata,
    ToolResult,
)

from app.tools.base import BaseTool


class CalculatorTool(BaseTool):
    """
    Perform mathematical calculations using SymPy.
    """

    def __init__(self):

        super().__init__(

            name=ToolName.CALCULATOR,

            metadata=ToolMetadata(

                description="Evaluate mathematical expressions accurately.",

                usage=[

                    "Arithmetic calculations",

                    "Addition",

                    "Subtraction",

                    "Multiplication",

                    "Division",

                    "Percentages",

                    "Scientific calculations",

                    "Algebraic expressions",

                    "Square roots",

                    "Powers"

                ],

                parameters={

                    "expression": "25*89"

                },

                examples=[

                    "25*89",

                    "(125+95)/5",

                    "sqrt(144)",

                    "2**10",

                    "sin(pi/2)",

                    "log(100)"

                ]

            )

        )

    def run(

        self,

        expression: str,

    ) -> ToolResult:

        try:

            value = sympify(

                expression

            ).evalf()

            result = CalculatorResult(

                expression=expression,

                result=str(value)

            )

            return ToolResult(

                success=True,

                tool_name=self.name,

                content=result

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

        result: ToolResult,

    ) -> str:

        if (

            not result.success

            or result.content is None

        ):

            return ""

        calc: CalculatorResult = result.content

        return f"""
Calculation Result

Expression:
{calc.expression}

Answer:
{calc.result}
""".strip()