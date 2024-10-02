from enum import StrEnum
from public import public


@public
class DataType(StrEnum):
    FLOAT = "float"
    INT = "integer"
    STR = "string"
    DATETIME = "datetime"
    BOOL = "boolean"


class Relationship(StrEnum):
    LINKS = "links_with"
