from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.model import InvokeError

from utils.redis_utils import get_redis_connection


class RedisExistsAction(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        key = tool_parameters.get('key')

        if not key:
            raise InvokeError('Missing required parameter: key')

        try:
            conn = get_redis_connection(self.runtime.credentials)
            exists = conn.exists(str(key))
        except Exception as e:
            raise InvokeError(f'Failed to check key in Redis: {e}') from e

        yield self.create_text_message('true' if exists else 'false')
