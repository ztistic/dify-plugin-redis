from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.model import InvokeError

from utils.redis_utils import get_redis_connection


def _parse_ttl(ttl_raw: Any) -> int:
    """Parse and validate the ttl parameter.

    Returns the TTL in seconds. Accepts -1 (no expiry) or a positive integer.
    Defaults to 60 when ttl is not provided.
    """
    ttl_raw = ttl_raw or 60
    try:
        ttl = int(ttl_raw)
    except (TypeError, ValueError):
        raise InvokeError(f'Invalid ttl: {ttl_raw}, must be an integer')
    if ttl != -1 and ttl <= 0:
        raise InvokeError(f'Invalid ttl: {ttl}, must be -1 or a positive integer')
    return ttl


class RedisSetAction(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        name = tool_parameters.get('name')
        key = tool_parameters.get('key')
        value = tool_parameters.get('value')

        if not name or not key or not value:
            raise InvokeError('Missing required parameters: name, key and value')

        ttl = _parse_ttl(tool_parameters.get('ttl'))

        try:
            redis_key = str(name) + ':' + str(key)
            value = str(value)
            conn = get_redis_connection(self.runtime.credentials)
            if ttl == -1:
                conn.set(redis_key, value)
            else:
                conn.setex(redis_key, ttl, value)
        except Exception as e:
            raise InvokeError(f'Failed to write to Redis: {e}') from e

        yield self.create_text_message(value)
