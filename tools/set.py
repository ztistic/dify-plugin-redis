from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.model import InvokeError

from utils.redis_utils import get_redis_connection, parse_ttl


class RedisSetAction(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        key = tool_parameters.get('key')
        value = tool_parameters.get('value')

        if not key or not value:
            raise InvokeError('Missing required parameters: key and value')

        ttl = parse_ttl(tool_parameters.get('ttl'))
        if ttl == -1:
            ttl = None

        try:
            conn = get_redis_connection(self.runtime.credentials)
            conn.set(str(key), str(value), ex=ttl)
        except Exception as e:
            raise InvokeError(f'Failed to write to Redis: {e}') from e

        yield self.create_text_message(str(value))
