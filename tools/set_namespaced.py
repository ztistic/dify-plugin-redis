from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.model import InvokeError

from utils.redis_utils import get_redis_connection, parse_ttl

DEFAULT_TTL = 60


class RedisSetNamespacedAction(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        name = tool_parameters.get('name')
        key = tool_parameters.get('key')
        value = tool_parameters.get('value')

        if not name or not key or not value:
            raise InvokeError('Missing required parameters: name, key and value')

        ttl = parse_ttl(tool_parameters.get('ttl'))
        if ttl is None:
            ttl = DEFAULT_TTL

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
