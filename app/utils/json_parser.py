import json
import re

from pydantic import BaseModel
from pydantic import ValidationError


class JsonParser:
    """
    Utility for parsing JSON responses returned by LLMs.

    Handles providers that wrap JSON inside Markdown
    code blocks.
    """

    @staticmethod
    def clean(text: str) -> str:
        """
        Remove Markdown code fences.
        """

        text = text.strip()

        # Remove opening ```json or ```
        text = re.sub(
            r"^```(?:json)?\s*",
            "",
            text,
            flags=re.IGNORECASE
        )

        # Remove closing ```
        text = re.sub(
            r"\s*```$",
            "",
            text
        )

        return text.strip()

    @staticmethod
    def to_dict(text: str) -> dict:
        """
        Convert cleaned JSON string into a dictionary.
        """

        text = JsonParser.clean(text)

        return json.loads(text)

    @staticmethod
    def to_model(
        text: str,
        model: type[BaseModel]
    ) -> BaseModel:
        """
        Convert LLM response into a Pydantic model.
        """

        try:

            data = JsonParser.to_dict(text)

            return model.model_validate(data)

        except json.JSONDecodeError as e:

            raise ValueError(
                f"Invalid JSON returned by LLM:\n\n{text}"
            ) from e

        except ValidationError as e:

            raise ValueError(
                f"JSON validation failed:\n\n{text}"
            ) from e