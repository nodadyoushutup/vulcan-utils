# medusa_logger/encoder.py
import json
import uuid
from datetime import date, datetime
from datetime import time as dt_time  # Alias for clarity
from decimal import Decimal
from enum import Enum
from typing import Any

try:
    # Import numpy and pandas only if available
    import numpy as np
    import pandas as pd
    HAS_NUMPY_PANDAS = True
except ImportError:
    HAS_NUMPY_PANDAS = False


class Encoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        """
        Override the default() method to serialize additional types.

        Args:
            obj: The object to be serialized.

        Returns:
            The serialized object, or calls the superclass's default method if the object
            does not match any known type.
        """

        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, dt_time):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        elif HAS_NUMPY_PANDAS:
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif 'pandas' in str(type(obj)):
                return obj.to_dict(orient='records')
        elif hasattr(obj, "__dict__"):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
