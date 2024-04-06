# tests/test_encoder.py
import json
from datetime import datetime, date, time
from decimal import Decimal
from enum import Enum
import uuid
from vulcan_logger.encoder import Encoder


class MockEnum(Enum):
    VALUE = 'test_value'


def test_encode_datetime() -> None:
    """
    Tests the JSON encoding of datetime objects.

    Ensures that datetime objects are correctly converted to an ISO formatted string
    when dumped to JSON using the custom Encoder.
    """

    obj = datetime(2022, 3, 4, 5, 6, 7)
    assert json.dumps(obj, cls=Encoder) == '"2022-03-04T05:06:07"'


def test_encode_date() -> None:
    """
    Tests the JSON encoding of date objects.

    Verifies that date objects are properly encoded to an ISO formatted date string
    when serialized to JSON using the custom Encoder.
    """

    obj = date(2022, 3, 4)
    assert json.dumps(obj, cls=Encoder) == '"2022-03-04"'


def test_encode_time() -> None:
    """
    Tests the JSON encoding of time objects.

    Checks that time objects are accurately converted to an ISO formatted time string
    in JSON output using the custom Encoder.
    """

    obj = time(5, 6, 7)
    assert json.dumps(obj, cls=Encoder) == '"05:06:07"'


def test_encode_decimal() -> None:
    """
    Tests the JSON encoding of Decimal objects.

    Asserts that Decimal objects are serialized to their numerical value in string
    form when using the custom Encoder to dump them to JSON.
    """

    obj = Decimal('12.34')
    assert json.dumps(obj, cls=Encoder) == '12.34'


def test_encode_enum() -> None:
    """
    Tests JSON encoding of Enum members.

    Ensures that Enum members are encoded to their value (a string representation)
    when serialized to JSON with the custom Encoder.
    """

    assert json.dumps(MockEnum.VALUE, cls=Encoder) == '"test_value"'


def test_encode_uuid() -> None:
    """
    Tests the JSON encoding of UUID objects.

    Verifies that UUID objects are correctly converted to their string representation
    when dumped to JSON using the custom Encoder.
    """

    obj = uuid.uuid4()
    assert json.dumps(obj, cls=Encoder) == f'"{str(obj)}"'
