from typing import Any

import redis
from redis.client import Redis
from rediscluster import RedisCluster

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 6379


def get_redis_cluster(data: dict[str, Any]) -> RedisCluster:
    return RedisCluster(
        startup_nodes=[{
            'host': data.get('host') or DEFAULT_HOST,
            'port': int(data.get('port') or DEFAULT_PORT)
        }],
        password=data.get('password'),
        decode_responses=True
    )


def get_redis_single(data: dict[str, Any]) -> Redis:
    return redis.Redis(connection_pool=redis.ConnectionPool(
        host=data.get('host') or DEFAULT_HOST,
        port=int(data.get('port') or DEFAULT_PORT),
        password=data.get('password'),
        decode_responses=True
    ))


def get_redis_connection(data: dict[str, Any]) -> RedisCluster | Redis:
    is_cluster = bool(data.get('cluster') or False)
    if is_cluster:
        return get_redis_cluster(data)
    else:
        return get_redis_single(data)
