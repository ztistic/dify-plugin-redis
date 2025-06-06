from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.redis_utils import get_redis_connection


class RedisSetAction(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        name = tool_parameters.get('name')
        key = tool_parameters.get('key')
        value = tool_parameters.get('value')
        ttl = int(tool_parameters.get('ttl') or 60)

        if name and key and value:
            redis_key = name + ':' + key
            conn = get_redis_connection(self.runtime.credentials)
            if -1 == ttl:
                conn.set(name=redis_key, value=value)
            else:
                conn.setex(redis_key, ttl, value)
        yield self.create_text_message(value)
