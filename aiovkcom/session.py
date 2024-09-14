"""Session."""
import logging
from typing import Any, Dict

from httpx import AsyncClient, Response

log = logging.getLogger(__name__)


class TokenSession:
    """Session for executing authorized requests."""

    __slots__ = ('v', 'access_token', 'client')

    def __init__(self, v: str, access_token: str) -> None:
        """Set credentials."""
        self.v = v
        self.access_token = access_token
        self.client = AsyncClient(
            default_encoding='application/json; charset=utf-8',
            base_url='https://api.vk.com/method/',
            follow_redirects=True,
        )

    async def request(
        self,
        method_name: str,
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Send a request.

        Args:
            method_name (str): method name
            params (Dict[str, Any]): query parameters

        Returns:
            Dict[str, Any]

        """
        params = {k: params[k] for k in params if params[k]}
        params['access_token'] = self.access_token
        params['v'] = self.v

        try:
            resp: Response = await self.client.get(method_name, params=params)
        except Exception:
            log.error(f'GET /{method_name} request failed')
            raise
        else:
            log.info(f'GET {resp.url} {resp.status_code}')

        resp.raise_for_status()

        try:
            return resp.json()
        except Exception:
            content = resp.read().decode()
            log.error(f'GET {resp.url} {resp.status_code}: {content}')
            raise
