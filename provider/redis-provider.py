import logging
from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from utils.redis_utils import get_redis_connection


log = logging.getLogger(__name__)


class RedisToolProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            conn = get_redis_connection(credentials)
            if response := conn.ping():
                log.info(f'connect to redis server success, {response=}')
        except Exception as e:
            log.exception(f'connect to redis server failed: {e}')
            raise ToolProviderCredentialValidationError(str(e))
