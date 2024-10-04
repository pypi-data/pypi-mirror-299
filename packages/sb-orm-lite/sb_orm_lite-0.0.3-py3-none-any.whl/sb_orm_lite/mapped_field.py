import datetime
import decimal
import uuid
from typing import Generic, TypeVar

T = TypeVar("T")


class FieldType(object):
    ...


class Integer(FieldType):
    ...


class String(FieldType):
    size: int

    def __init__(self, size: int = 50):
        self.size = size


class Float(FieldType):
    ...


class Decimal(FieldType):
    size: int
    scale: int

    def __init__(self, size: int = 0, scale: int = 0):
        self.size = size
        self.scale = scale


class GUID(FieldType):
    ...


class DateTime(FieldType):
    ...


class Mapped(Generic[T]):
    name: str
    field_name: str
    field_type: FieldType
    value: T
    size: int
    precision: int
    primary_key: bool
    auto_increment: bool
    unique: bool
    optional: bool
    default: T
    ignore: bool

    def __str__(self):
        return str(self.value)


def mapped_column(name: str = None, field_name: str = None, field_type: FieldType = Integer, size: int = 0, precision: int = 0, primary_key: bool = False,
                  autoincrement: bool = False, unique: bool = False,
                  optional: bool = False,
                  default: T = None, ignore: bool = False) -> Mapped[T]:
    base_field_type: T = int
    if field_type is Integer:
        base_field_type = int
    elif field_type is String:
        base_field_type = str
    elif field_type is Float:
        base_field_type = float
    elif field_type is Decimal:
        base_field_type = decimal.Decimal
    elif field_type is GUID:
        base_field_type = uuid.UUID
    elif field_type is DateTime:
        base_field_type = datetime.datetime

    mapped = Mapped[base_field_type]()
    mapped.name = name
    mapped.field_name = field_name
    mapped.primary_key = primary_key
    mapped.auto_increment = autoincrement
    mapped.field_type = field_type
    mapped.size = size
    mapped.precision = precision
    mapped.unique = unique
    mapped.optional = optional
    mapped.default = default
    mapped.ignore = ignore

    return mapped
