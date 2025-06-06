from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.redis_utils import get_redis_connection


class RedisGetAction(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        name = tool_parameters.get('name')
        key = tool_parameters.get('key')

        if name and key:
            conn = get_redis_connection(self.runtime.credentials)
            value = conn.get(name + ':' + key)
            yield self.create_text_message(value or '')
        yield self.create_text_message('')
