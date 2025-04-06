import os
import logging
import redis
from typing import Optional

logger = logging.getLogger("app")

def get_redis_connection() -> Optional[redis.Redis]:
    """
    Create and return a Redis connection based on environment variables.
    Returns None if connection fails or is not configured.
    """
    try:
        if os.getenv("AZURE_REDIS_CONNECTIONSTRING"):
            # Parse Azure Redis connection string
            logger.info("Connecting to Azure Redis Cache...")
            conn_str = os.getenv("AZURE_REDIS_CONNECTIONSTRING")
            if conn_str.startswith("rediss://"):
                # Handle SSL connection
                parsed = conn_str.replace("rediss://:", "").split("@")
                password = parsed[0]
                host_port = parsed[1].split("/")[0]
                host, port = host_port.split(":")
                
                return redis.Redis(
                    host=host,
                    port=int(port),
                    password=password,
                    ssl=True,
                    decode_responses=True
                )
            else:
                # For non-SSL connections or other formats
                logger.warning("Unsupported Redis connection string format")
                return None
        else:
            # Local Redis connection
            logger.info("Connecting to local Redis server...")
            redis_host = os.environ.get("REDIS_HOST", "localhost")
            redis_port = int(os.environ.get("REDIS_PORT", 6379))
            
            return redis.Redis(
                host=redis_host,
                port=redis_port,
                decode_responses=True
            )
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {str(e)}")
        return None

def cache_get(redis_client: redis.Redis, key: str) -> Optional[str]:
    """Get a value from the Redis cache"""
    if not redis_client:
        return None
    try:
        return redis_client.get(key)
    except Exception as e:
        logger.error(f"Redis get error: {str(e)}")
        return None

def cache_set(redis_client: redis.Redis, key: str, value: str, expire_seconds: int = 3600) -> bool:
    """Set a value in the Redis cache with expiration"""
    if not redis_client:
        return False
    try:
        return redis_client.set(key, value, ex=expire_seconds)
    except Exception as e:
        logger.error(f"Redis set error: {str(e)}")
        return False
