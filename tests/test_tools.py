from unittest.mock import MagicMock, patch

import pytest

from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.model import InvokeError
from tools.redis_get import RedisGetAction
from tools.redis_set import RedisSetAction


def make_tool(cls, credentials=None):
    """构造工具实例，绕过 Tool.__init__，仅提供测试所需的 runtime/response_type。"""
    tool = cls.__new__(cls)
    tool.runtime = type('Runtime', (), {'credentials': credentials or {}})()
    tool.response_type = ToolInvokeMessage
    return tool


class TestRedisSetAction:
    @pytest.mark.parametrize(
        'params',
        [
            {'name': '', 'key': 'k', 'value': 'v'},
            {'name': 'n', 'key': '', 'value': 'v'},
            {'name': 'n', 'key': 'k', 'value': ''},
        ],
    )
    def test_missing_params_raise(self, params):
        tool = make_tool(RedisSetAction)
        with pytest.raises(InvokeError):
            list(tool._invoke(params))

    def test_ttl_minus_one_uses_set(self):
        tool = make_tool(RedisSetAction)
        conn = MagicMock()
        with patch('tools.redis_set.get_redis_connection', return_value=conn):
            msgs = list(tool._invoke({'name': 'n', 'key': 'k', 'value': 'v', 'ttl': -1}))
        assert len(msgs) == 1
        conn.set.assert_called_once_with('n:k', 'v')
        conn.setex.assert_not_called()

    def test_default_ttl_uses_setex(self):
        tool = make_tool(RedisSetAction)
        conn = MagicMock()
        with patch('tools.redis_set.get_redis_connection', return_value=conn):
            list(tool._invoke({'name': 'n', 'key': 'k', 'value': 'v'}))
        conn.setex.assert_called_once_with('n:k', 60, 'v')
        conn.set.assert_not_called()

    def test_non_string_params_normalized(self):
        tool = make_tool(RedisSetAction)
        conn = MagicMock()
        with patch('tools.redis_set.get_redis_connection', return_value=conn):
            list(tool._invoke({'name': 123, 'key': 456, 'value': 789, 'ttl': -1}))
        conn.set.assert_called_once_with('123:456', '789')


class TestRedisGetAction:
    @pytest.mark.parametrize('params', [{'name': '', 'key': 'k'}, {'name': 'n', 'key': ''}])
    def test_missing_params_raise(self, params):
        tool = make_tool(RedisGetAction)
        with pytest.raises(InvokeError):
            list(tool._invoke(params))

    def test_yields_single_message(self):
        tool = make_tool(RedisGetAction)
        conn = MagicMock()
        conn.get.return_value = 'hello'
        with patch('tools.redis_get.get_redis_connection', return_value=conn):
            msgs = list(tool._invoke({'name': 'n', 'key': 'k'}))
        assert len(msgs) == 1  # 双 yield 已修复：只返回一条消息
        conn.get.assert_called_once_with('n:k')

    def test_missing_key_returns_empty(self):
        tool = make_tool(RedisGetAction)
        conn = MagicMock()
        conn.get.return_value = None
        with patch('tools.redis_get.get_redis_connection', return_value=conn):
            msgs = list(tool._invoke({'name': 'n', 'key': 'k'}))
        assert len(msgs) == 1
        text = getattr(msgs[0].message, 'text', msgs[0].message)
        assert text == ''
