from unittest.mock import MagicMock, patch

import pytest

from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.model import InvokeError
from tools.get import RedisGetAction
from tools.get_namespaced import RedisGetNamespacedAction
from tools.delete import RedisDelAction
from tools.set import RedisSetAction
from tools.set_namespaced import RedisSetNamespacedAction


def make_tool(cls, credentials=None):
    """构造工具实例，绕过 Tool.__init__，仅提供测试所需的 runtime/response_type。"""
    tool = cls.__new__(cls)
    tool.runtime = type('Runtime', (), {'credentials': credentials or {}})()
    tool.response_type = ToolInvokeMessage
    return tool


class TestRedisSetNamespacedAction:
    @pytest.mark.parametrize(
        'params',
        [
            {'name': '', 'key': 'k', 'value': 'v'},
            {'name': 'n', 'key': '', 'value': 'v'},
            {'name': 'n', 'key': 'k', 'value': ''},
        ],
    )
    def test_missing_params_raise(self, params):
        tool = make_tool(RedisSetNamespacedAction)
        with pytest.raises(InvokeError):
            list(tool._invoke(params))

    def test_ttl_minus_one_uses_set(self):
        tool = make_tool(RedisSetNamespacedAction)
        conn = MagicMock()
        with patch('tools.set_namespaced.get_redis_connection', return_value=conn):
            msgs = list(tool._invoke({'name': 'n', 'key': 'k', 'value': 'v', 'ttl': -1}))
        assert len(msgs) == 1
        conn.set.assert_called_once_with('n:k', 'v')
        conn.setex.assert_not_called()

    def test_default_ttl_uses_setex(self):
        tool = make_tool(RedisSetNamespacedAction)
        conn = MagicMock()
        with patch('tools.set_namespaced.get_redis_connection', return_value=conn):
            list(tool._invoke({'name': 'n', 'key': 'k', 'value': 'v'}))
        conn.setex.assert_called_once_with('n:k', 60, 'v')
        conn.set.assert_not_called()

    def test_non_string_params_normalized(self):
        tool = make_tool(RedisSetNamespacedAction)
        conn = MagicMock()
        with patch('tools.set_namespaced.get_redis_connection', return_value=conn):
            list(tool._invoke({'name': 123, 'key': 456, 'value': 789, 'ttl': -1}))
        conn.set.assert_called_once_with('123:456', '789')


class TestRedisSetAction:
    @pytest.mark.parametrize('params', [{'key': '', 'value': 'v'}, {'key': 'k', 'value': ''}])
    def test_missing_params_raise(self, params):
        tool = make_tool(RedisSetAction)
        with pytest.raises(InvokeError):
            list(tool._invoke(params))

    def test_default_no_expiry(self):
        tool = make_tool(RedisSetAction)
        conn = MagicMock()
        with patch('tools.set.get_redis_connection', return_value=conn):
            msgs = list(tool._invoke({'key': 'k', 'value': 'v'}))
        conn.set.assert_called_once_with('k', 'v', ex=None)
        text = getattr(msgs[0].message, 'text', msgs[0].message)
        assert text == 'v'

    def test_ttl_uses_ex(self):
        tool = make_tool(RedisSetAction)
        conn = MagicMock()
        with patch('tools.set.get_redis_connection', return_value=conn):
            list(tool._invoke({'key': 'k', 'value': 'v', 'ttl': 120}))
        conn.set.assert_called_once_with('k', 'v', ex=120)


class TestRedisGetNamespacedAction:
    @pytest.mark.parametrize('params', [{'name': '', 'key': 'k'}, {'name': 'n', 'key': ''}])
    def test_missing_params_raise(self, params):
        tool = make_tool(RedisGetNamespacedAction)
        with pytest.raises(InvokeError):
            list(tool._invoke(params))

    def test_yields_single_message(self):
        tool = make_tool(RedisGetNamespacedAction)
        conn = MagicMock()
        conn.get.return_value = 'hello'
        with patch('tools.get_namespaced.get_redis_connection', return_value=conn):
            msgs = list(tool._invoke({'name': 'n', 'key': 'k'}))
        assert len(msgs) == 1  # 双 yield 已修复：只返回一条消息
        conn.get.assert_called_once_with('n:k')

    def test_missing_key_returns_empty(self):
        tool = make_tool(RedisGetNamespacedAction)
        conn = MagicMock()
        conn.get.return_value = None
        with patch('tools.get_namespaced.get_redis_connection', return_value=conn):
            msgs = list(tool._invoke({'name': 'n', 'key': 'k'}))
        assert len(msgs) == 1
        text = getattr(msgs[0].message, 'text', msgs[0].message)
        assert text == ''


class TestRedisDelAction:
    def test_missing_key_param_raises(self):
        tool = make_tool(RedisDelAction)
        with pytest.raises(InvokeError):
            list(tool._invoke({'key': ''}))

    def test_existing_key_returns_one(self):
        tool = make_tool(RedisDelAction)
        conn = MagicMock()
        conn.delete.return_value = 1
        with patch('tools.delete.get_redis_connection', return_value=conn):
            msgs = list(tool._invoke({'key': 'k'}))
        assert len(msgs) == 1
        conn.delete.assert_called_once_with('k')
        text = getattr(msgs[0].message, 'text', msgs[0].message)
        assert text == '1'

    def test_missing_key_returns_zero(self):
        tool = make_tool(RedisDelAction)
        conn = MagicMock()
        conn.delete.return_value = 0
        with patch('tools.delete.get_redis_connection', return_value=conn):
            msgs = list(tool._invoke({'key': 'k'}))
        text = getattr(msgs[0].message, 'text', msgs[0].message)
        assert text == '0'


class TestRedisGetAction:
    def test_missing_key_param_raises(self):
        tool = make_tool(RedisGetAction)
        with pytest.raises(InvokeError):
            list(tool._invoke({'key': ''}))

    def test_yields_single_message(self):
        tool = make_tool(RedisGetAction)
        conn = MagicMock()
        conn.get.return_value = 'hello'
        with patch('tools.get.get_redis_connection', return_value=conn):
            msgs = list(tool._invoke({'key': 'k'}))
        assert len(msgs) == 1
        conn.get.assert_called_once_with('k')

    def test_missing_key_returns_empty(self):
        tool = make_tool(RedisGetAction)
        conn = MagicMock()
        conn.get.return_value = None
        with patch('tools.get.get_redis_connection', return_value=conn):
            msgs = list(tool._invoke({'key': 'k'}))
        assert len(msgs) == 1
        text = getattr(msgs[0].message, 'text', msgs[0].message)
        assert text == ''
