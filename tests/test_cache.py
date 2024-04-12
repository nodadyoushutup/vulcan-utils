# test/test_cache.py
import pytest
from unittest.mock import MagicMock, patch
from redis.exceptions import RedisError
from vulcan_utils.cache import Cache
import json


@pytest.fixture
def mock_redis():
    with patch('redis.Redis') as mock:
        yield mock


def test_cache_init_success(mock_redis):
    """ Test initializing the Cache class successfully connects to Redis. """
    mock_redis.return_value.ping.return_value = True
    cache = Cache()
    assert cache is not None


def test_cache_init_failure(mock_redis):
    """ Test Cache initialization fails when Redis connection cannot be established. """
    mock_redis.return_value.ping.side_effect = RedisError("Connection refused")
    with pytest.raises(RedisError):
        cache = Cache()


def test_set_key_success(mock_redis):
    """ Test setting a key in Redis cache successfully. """
    mock_redis.return_value.set.return_value = True
    cache = Cache()
    cache.set("test_key", {"data": "value"}, expire=3600)


def test_get_key_success(mock_redis):
    """ Test getting a key from Redis cache successfully. """
    mock_redis.return_value.get.return_value = json.dumps({"data": "value"})
    cache = Cache()
    result = cache.get("test_key")
    assert result == {"data": "value"}


def test_delete_key_success(mock_redis):
    """ Test deleting a key from Redis cache successfully. """
    mock_redis.return_value.delete.return_value = 1
    cache = Cache()
    cache.delete("test_key")


def test_clear_cache_success(mock_redis):
    """ Test clearing all keys from Redis cache successfully. """
    mock_redis.return_value.flushdb.return_value = True
    cache = Cache()
    cache.clear()


def test_set_key_failure(mock_redis):
    """ Test failure in setting a key raises an exception. """
    mock_redis.return_value.set.side_effect = RedisError(
        "Write operation failed")
    cache = Cache()
    with pytest.raises(RedisError):
        cache.set("test_key", {"data": "value"})


def test_get_key_failure(mock_redis):
    """ Test failure in getting a key raises an exception. """
    mock_redis.return_value.get.side_effect = RedisError(
        "Read operation failed")
    cache = Cache()
    with pytest.raises(RedisError):
        cache.get("test_key")


def test_delete_key_failure(mock_redis):
    """ Test failure in deleting a key raises an exception. """
    mock_redis.return_value.delete.side_effect = RedisError(
        "Delete operation failed")
    cache = Cache()
    with pytest.raises(RedisError):
        cache.delete("test_key")


def test_clear_cache_failure(mock_redis):
    """ Test failure in clearing the cache raises an exception. """
    mock_redis.return_value.flushdb.side_effect = RedisError(
        "Clear operation failed")
    cache = Cache()
    with pytest.raises(RedisError):
        cache.clear()
