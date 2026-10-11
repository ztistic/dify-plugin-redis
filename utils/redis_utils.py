from typing import Any

import redis
from dify_plugin.errors.model import InvokeError
from redis import Redis
from redis.cluster import ClusterNode, RedisCluster

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 6379
DEFAULT_DB = 0


def parse_ttl(ttl_raw: Any) -> int | None:
    """Parse and validate a ttl parameter.

    Returns None when ttl is not provided or falsy (callers decide the default
    policy), -1 for no expiry, or a positive integer in seconds.
    """
    if not ttl_raw:
        return None
    try:
        ttl = int(ttl_raw)
    except (TypeError, ValueError):
        raise InvokeError(f'Invalid ttl: {ttl_raw}, must be an integer')
    if ttl != -1 and ttl <= 0:
        raise InvokeError(f'Invalid ttl: {ttl}, must be -1 or a positive integer')
    return ttl


def get_redis_cluster(data: dict[str, Any]) -> RedisCluster:
    return RedisCluster(
        startup_nodes=[ClusterNode(
            data.get('host') or DEFAULT_HOST,
            int(data.get('port') or DEFAULT_PORT),
        )],
        password=data.get('password'),
        decode_responses=True,
    )


def get_redis_single(data: dict[str, Any]) -> Redis:
    return redis.Redis(connection_pool=redis.ConnectionPool(
        host=data.get('host') or DEFAULT_HOST,
        port=int(data.get('port') or DEFAULT_PORT),
        db=int(data.get('db') or DEFAULT_DB),
        password=data.get('password'),
        decode_responses=True
    ))


def get_redis_connection(data: dict[str, Any]) -> RedisCluster | Redis:
    is_cluster = bool(data.get('cluster') or False)
    if is_cluster:
        return get_redis_cluster(data)
    else:
        return get_redis_single(data)
