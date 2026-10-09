from unittest.mock import patch

from utils import redis_utils


class TestGetRedisConnection:
    def test_single_when_cluster_false(self):
        with patch('utils.redis_utils.redis.Redis') as MockRedis:
            redis_utils.get_redis_connection({'cluster': False})
            MockRedis.assert_called_once()

    def test_single_when_cluster_missing(self):
        with patch('utils.redis_utils.redis.Redis') as MockRedis:
            redis_utils.get_redis_connection({})
            MockRedis.assert_called_once()

    def test_cluster_when_cluster_true(self):
        with patch('utils.redis_utils.RedisCluster') as MockCluster:
            redis_utils.get_redis_connection({'cluster': True})
            MockCluster.assert_called_once()


class TestGetRedisSingle:
    def test_defaults_applied(self):
        with patch('utils.redis_utils.redis.Redis'), \
                patch('utils.redis_utils.redis.ConnectionPool') as MockPool:
            redis_utils.get_redis_single({})
            MockPool.assert_called_once()
            kwargs = MockPool.call_args.kwargs
            assert kwargs['host'] == '127.0.0.1'
            assert kwargs['port'] == 6379
            assert kwargs['db'] == 0

    def test_custom_params(self):
        with patch('utils.redis_utils.redis.Redis'), \
                patch('utils.redis_utils.redis.ConnectionPool') as MockPool:
            redis_utils.get_redis_single({'host': 'h', 'port': '6380', 'db': '2', 'password': 'p'})
            kwargs = MockPool.call_args.kwargs
            assert kwargs['host'] == 'h'
            assert kwargs['port'] == 6380
            assert kwargs['db'] == 2
            assert kwargs['password'] == 'p'


class TestGetRedisCluster:
    def test_startup_nodes_and_password(self):
        with patch('utils.redis_utils.RedisCluster') as MockCluster:
            redis_utils.get_redis_cluster({'host': 'h', 'port': '7000', 'password': 'p'})
            MockCluster.assert_called_once()
            kwargs = MockCluster.call_args.kwargs
            startup_nodes = kwargs['startup_nodes']
            assert len(startup_nodes) == 1
            assert startup_nodes[0].host == 'h'
            assert startup_nodes[0].port == 7000
            assert kwargs['password'] == 'p'
            assert kwargs['decode_responses'] is True
