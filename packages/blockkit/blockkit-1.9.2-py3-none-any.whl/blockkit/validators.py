from collections.abc import Callable
from datetime import date, datetime, time
from typing import TYPE_CHECKING, Optional, Union

from pydantic import field_validator

if TYPE_CHECKING:
    from blockkit.objects import MarkdownText, PlainText


def validator(
    field: str, func: Callable, each_item: bool = False, **kwargs
) -> classmethod:
    return field_validator(field)(lambda v: func(v, **kwargs))


def validate_text_length(
    v: Union["PlainText", "MarkdownText", str], *, max_length: int
) -> Union["PlainText", "MarkdownText", str]:
    if v is not None:
        e = ValueError(f"Maximum length is {max_length} characters")
        if type(v) == str and len(v) > max_length:
            raise e
        elif type(v) != str and len(getattr(v, "text")) > max_length:
            raise e
    return v


def validate_list_text_length(v, *, max_length: int):
    if v is not None:
        for item in v:
            validate_text_length(item, max_length=max_length)
    return v


def validate_date(v: date) -> Optional[str]:
    if v is not None:
        return v.isoformat()
    return v


def validate_time(v: time) -> Optional[str]:
    if v is not None:
        return v.strftime("%H:%M")
    return v


def validate_datetime(v: Union[int, datetime]) -> Optional[int]:
    if v is not None:
        if type(v) == datetime:
            return int(v.timestamp())
        else:
            _ = datetime.fromtimestamp(v)
            return v
    return v

