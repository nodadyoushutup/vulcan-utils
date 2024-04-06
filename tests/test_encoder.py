# tests/test_encoder.py
import json
from datetime import datetime, date, time
from decimal import Decimal
from enum import Enum
import uuid
from medusa_logger.encoder import Encoder


class MockEnum(Enum):
    VALUE = 'test_value'


def test_encode_datetime():
    obj = datetime(2022, 3, 4, 5, 6, 7)
    assert json.dumps(obj, cls=Encoder) == '"2022-03-04T05:06:07"'


def test_encode_date():
    obj = date(2022, 3, 4)
    assert json.dumps(obj, cls=Encoder) == '"2022-03-04"'


def test_encode_time():
    obj = time(5, 6, 7)
    assert json.dumps(obj, cls=Encoder) == '"05:06:07"'


def test_encode_decimal():
    obj = Decimal('12.34')
    assert json.dumps(obj, cls=Encoder) == '12.34'


def test_encode_enum():
    assert json.dumps(MockEnum.VALUE, cls=Encoder) == '"test_value"'


def test_encode_uuid():
    obj = uuid.uuid4()
    assert json.dumps(obj, cls=Encoder) == f'"{str(obj)}"'
