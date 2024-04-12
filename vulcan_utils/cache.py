from typing import Any, Optional
import redis
import json
from vulcan_utils.encoder import Encoder
from redis.exceptions import RedisError, ConnectionError


class Cache:
    def __init__(self, host="localhost", port=6379, db=0):
        """
        Initializes the Cache object with a Redis connection.
        Raises a ConnectionError if the Redis server cannot be reached.

        Args:
            host (str): The hostname of the Redis server.
            port (int): The port number on which the Redis server is running.
            db (int): The database number to connect to.
        """
        try:
            self.redis = redis.Redis(host=host, port=port, db=db)
            self.redis.ping()  # Try to ping the server to check connection
        except ConnectionError as e:
            raise ConnectionError(f"Failed to connect to Redis: {str(e)}")

    def set(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        """
        Stores a value in the cache, optionally setting an expiration time.

        Args:
            key (str): The key under which the value is stored.
            value (Any): The value to be stored.
            expire (Optional[int]): The expiration time in seconds. If not specified, the value does not expire.

        Raises:
            RedisError: If the operation cannot be completed.
        """
        try:
            serialized_value = json.dumps(value, cls=Encoder)
            self.redis.set(key, serialized_value, ex=expire)
        except RedisError as e:
            raise RedisError(f"Failed to set key {key}: {str(e)}")

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieves a value from the cache.

        Args:
            key (str): The key for which the value is retrieved.

        Returns:
            Optional[Any]: The retrieved value or None if the key does not exist.

        Raises:
            RedisError: If the operation cannot be completed.
        """
        try:
            serialized_value = self.redis.get(key)
            if serialized_value is not None:
                return json.loads(serialized_value)
        except RedisError as e:
            raise RedisError(f"Failed to get key {key}: {str(e)}")
        return None

    def delete(self, key: str) -> None:
        """
        Deletes a specific key from the cache.

        Args:
            key (str): The key to be deleted.

        Raises:
            RedisError: If the operation cannot be completed.
        """
        try:
            self.redis.delete(key)
        except RedisError as e:
            raise RedisError(f"Failed to delete key {key}: {str(e)}")

    def clear(self) -> None:
        """
        Clears all keys and values from the current database.

        Raises:
            RedisError: If the operation cannot be completed.
        """
        try:
            self.redis.flushdb()
        except RedisError as e:
            raise RedisError("Failed to clear database: {str(e)}")
