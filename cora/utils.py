import re
import time
import logging
from typing import Any, Dict, Text

logger = logging.getLogger(__name__)

camelCase = re.compile(r"(?<!^)(?=[A-Z])")


def unix_epoch() -> float:
    return time.time()


def convert_model_to_snake_case(d: Dict[Text, Any]) -> Dict[Text, Any]:
    return {convert_camel_to_snake(k): v for k, v in d.items()}


def convert_camel_to_snake(s: Text) -> Text:
    return camelCase.sub("_", s).lower()


def convert_snake_to_camel(s: Text) -> Text:
    return "".join(word.title() for word in s.split("_"))


def normalize_phone_number(phone_number: Text) -> Text:
    if phone_number == None or len(phone_number) > 15:
        phone_number = "2065551212"
    chars_to_replace = ["+", "-", "(", ")", "."]
    for char in chars_to_replace:
        phone_number = phone_number.replace(char, "")
    return phone_number
