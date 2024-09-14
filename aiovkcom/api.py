"""vk.com API."""
from typing import Any, Dict, Generator, Tuple

from .session import TokenSession


class API:
    """vk.com API.

    Attributes:
        session (TokenSession): session.

    """

    __slots__ = ('session', )

    def __init__(self, v: str, access_token: str) -> None:
        """Set session."""
        self.session = TokenSession(v=v, access_token=access_token)

    def __await__(self) -> Generator['API', None, None]:
        """Await self."""
        yield self

    async def __aenter__(self) -> 'API':
        """Enter."""
        return self

    async def __aexit__(self, *args: Tuple[Any, Any, Any]) -> None:
        """Exit."""
        if self.session.client.is_closed is False:
            await self.session.client.aclose()

    def __getattr__(self, name) -> 'APIMethod':
        """Return an API method."""
        return APIMethod(self, name)

    async def __call__(self, name: str, **params: Dict[str, Any]) -> 'APIMethod':  # noqa
        """Call an API method by its name.

        Args:
            name (str): full method's name
            params (Dict[str, Any]): query parameters

        Return:
            APIMethod

        """
        return await getattr(self, name)(**params)


class APIMethod:
    """vk.com REST API method.

    Attributes:
        api (API): API instance
        name (str): full method's name

    """

    __slots__ = ('api', 'name')

    def __init__(self, api: API, name: str) -> None:
        """Set method name."""
        self.api = api
        self.name = name

    def __getattr__(self, name: str) -> 'APIMethod':
        """Chain methods.

        Args:
            name (str): method name

        """
        return APIMethod(self.api, self.name + '.' + name)

    async def __call__(self, **params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a request.

        Args:
            params (Dict[str, Any]): query parameters

        Returns:
            Dict[str, Any]

        """
        return await self.api.session.request(self.name, params)
