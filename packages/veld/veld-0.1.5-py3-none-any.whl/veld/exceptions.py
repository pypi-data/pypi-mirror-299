# -*- coding: utf-8 -*-

"""Exceptions

This file is part of the Veld package.

Author: G.J.J. van den Burg
License: See the LICENSE file
Copyright: (c) 2022, G.J.J. van den Burg

"""

from typing import Any


class Error(Exception):
    """Base class for exceptions in Veld"""


class StreamProcessingError(Error):
    """Exception for processing errors in the data stream"""

    def __init__(self, value: Any) -> None:
        self._value = value

    def __str__(self) -> str:
        msg = (
            f"ERROR: Couldn't parse value: {self._value}\n\n"
            "Use the -i / --ignore option to skip such values."
        )
        return msg


class InvalidInputError(Error):
    """Exception raised when invalid input is supplied to the command"""

    def __init__(self, reason: str) -> None:
        self._reason = reason

    def __str__(self) -> str:
        msg = f"ERROR: Invalid input received: {self._reason}"
        return msg


class EmptyStreamError(Error):
    """Exception raised when no data was received"""

    pass
