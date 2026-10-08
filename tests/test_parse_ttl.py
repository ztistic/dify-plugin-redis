import pytest

from dify_plugin.errors.model import InvokeError
from tools.redis_set import _parse_ttl


class TestParseTTL:
    @pytest.mark.parametrize(
        ('raw', 'expected'),
        [
            (None, 60),      # 未传 → 默认 60
            (0, 60),         # 0 → 默认 60
            ('', 60),        # 空字符串 → 默认 60
            ({}, 60),        # 空容器（falsy）→ 默认 60
            ([], 60),        # 空列表（falsy）→ 默认 60
            (-1, -1),        # 永不过期
            (60, 60),        # 正常正数
            ('120', 120),    # 数字字符串
            (60.0, 60),      # 浮点整数值
        ],
    )
    def test_valid_values(self, raw, expected):
        assert _parse_ttl(raw) == expected

    @pytest.mark.parametrize(
        'raw',
        ['60s', 'abc', '1.5', -2, -5, 'nan', 'inf', [1, 2], {'a': 1}],
    )
    def test_invalid_values_raise(self, raw):
        with pytest.raises(InvokeError):
            _parse_ttl(raw)

    def test_float_is_truncated_to_int(self):
        # 已接受的行为：浮点 TTL 被截断为整数（Redis 不支持浮点 TTL）
        assert _parse_ttl(1.5) == 1
