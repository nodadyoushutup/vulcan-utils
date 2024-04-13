"""
vulcan_utils/encoder.py

This module provides decorators for logging, retrying, JSON serialization, rate limiting, 
and environment variable restriction for function execution.

Classes:
    - Encoder: A custom JSON encoder.
"""

import json
import uuid
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import Any


class Encoder(json.JSONEncoder):
    """
    JSON encoder with custom serialization for specific types.
    """

    def default(self, o: Any) -> Any:
        """
        Override the default() method to serialize additional types.

        Args:
            o: The object to be serialized.

        Returns:
            The serialized object, or calls the superclass's default method if the object
            does not match any known type.
        """

        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, date):
            return o.isoformat()
        elif isinstance(o, time):
            return o.isoformat()
        elif isinstance(o, Decimal):
            return float(o)
        elif isinstance(o, Enum):
            return o.value
        elif isinstance(o, uuid.UUID):
            return str(o)
        elif hasattr(o, "__dict__"):
            return {key: self.default(value) for key, value in o.__dict__.items()}
        else:
            return str(o)
