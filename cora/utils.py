import re
from typing import Any, Dict, Text

camelCase = re.compile(r"(?<!^)(?=[A-Z])")


def convert_model_to_snake_case(d: Dict[Text, Any]) -> Dict[Text, Any]:
    return {convert_camel_to_snake(k): v for k, v in d.items()}


def convert_camel_to_snake(s: Text) -> Text:
    return camelCase.sub("_", s).lower()


def convert_snake_to_camel(s: Text) -> Text:
    return "".join(word.title() for word in s.split("_"))

