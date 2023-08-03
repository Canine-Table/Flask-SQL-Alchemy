from wtforms.validators import ValidationError,StopValidation
from typing_extensions import (
    Concatenate,
    Literal,
    LiteralString,
    ParamSpec,
    Self,
    SupportsIndex,
    TypeAlias,
    TypeGuard,
    TypeVarTuple,
    final,
)

from typing import (
    IO,
    Any,
    BinaryIO,
    ClassVar,
    Generic,
    Mapping,
    MutableMapping,
    MutableSequence,
    NoReturn,
    Protocol,
    Sequence,
    SupportsAbs,
    SupportsBytes,
    SupportsComplex,
    SupportsFloat,
    SupportsInt,
    TypeVar,
    overload
)

from flask import flash


class QueryException(Exception):
    error_messages = []

    @classmethod
    def add_error_message(cls,error):
        cls.error_messages.append(error)

    @classmethod
    def error_count(cls):
        return bool(len(cls.error_messages) > 0)

    @classmethod
    def show_error_messages(cls):
        for error in cls.error_messages:
            flash(f"{error}", category='danger')
        raise QueryException

    @classmethod
    def clear_errors(cls):
        cls.error_messages = []


# class FormValidationError(QueryException,ValueError,):
#     def __init__(self, message="", *args, **kwargs):
#         ValueError.__init__(self, message, *args, **kwargs)











    # "DataRequired",
    # "Email",
    # "EqualTo",
    # "IPAddress",
    # "InputRequired",
    # "Length",
    # "NumberRange",
    # "Optional",
    # "Regexp",
    # "URL",
    # "AnyOf",
    # "NoneOf",
    # "MacAddress",
    # "UUID",
    # "ValidationError",
    # "StopValidation",
