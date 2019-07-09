"""vk.com API."""

from .sessions import TokenSession


class API:
    """vk.com REST API."""

    __slots__ = ('session', )

    def __init__(self, session: TokenSession):
        self.session = session

    def __getattr__(self, name):
        return APIMethod(self, name)

    async def __call__(self, name, **params):
        return await getattr(self, name)(**params)


class APIMethod:
    """vk.com REST API method."""

    __slots__ = ('api', 'name')

    def __init__(self, api: API, name: str):
        self.api = api
        self.name = name

    def __getattr__(self, name):
        return APIMethod(self.api, f'{self.name}.{name}')

    async def __call__(self, **params):
        return await self.api.session.request(self.name, params)
