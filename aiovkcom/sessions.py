import aiohttp
import asyncio
import logging
from yarl import URL

from .exceptions import APIError, AuthError
from .parsers import AuthPageParser, AccessPageParser


log = logging.getLogger(__name__)


class Session:
    """A wrapper around aiohttp.ClientSession."""

    CONTENT_TYPE = 'application/json; charset=utf-8'

    __slots__ = ('session', )

    def __init__(self, session=None):
        self.session = session or aiohttp.ClientSession()

    def __await__(self):
        return self.authorize().__await__()

    async def __aenter__(self):
        return await self.authorize()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def authorize(self):
        return self

    async def close(self):
        await self.session.close()


class TokenSession(Session):
    """Session for sending authorized requests."""

    URL = 'https://api.vk.com/method/'
    V = '5.101'

    __slots__ = ('access_token', 'v')

    def __init__(self, access_token, v='', session=None):
        super().__init__(session)
        self.access_token = access_token
        self.v = v or self.V

    @property
    def required_params(self):
        """Required parameters."""
        return {'v': self.v, 'access_token': self.access_token}

    async def request(self, method_name, params=()):
        """Sends a request.

        Args:
            method_name (str): method's name.
            params (dict): URL parameters.

        Returns:
            response (dict): JSON object response.

        """

        url = f'{self.URL}/{method_name}'
        params = {k: params[k] for k in params if params[k]}
        params.update(self.required_params)

        async with self.session.get(url, params=params) as resp:
            status = resp.status
            response = await resp.json(content_type=self.CONTENT_TYPE)

        if 'response' in response:
            response = response['response']
        elif 'error' in response:
            raise APIError(response['error'])
        else:
            raise RuntimeError(status)

        return response


class ImplicitSession(TokenSession):

    OAUTH_URL = 'https://oauth.vk.com/authorize'
    REDIRECT_URI = 'https://oauth.vk.com/blank.html'

    __slots__ = ('app_id', 'login', 'passwd', 'scope', 'expires_in')

    def __init__(self, app_id, login, passwd, scope='', v='', session=None):
        super().__init__('', v, session)
        self.app_id = app_id
        self.login = login
        self.passwd = passwd
        self.scope = scope

    @property
    def params(self):
        """Authorization parameters."""
        return {
            'display': 'page',
            'response_type': 'token',
            'redirect_uri': self.REDIRECT_URI,
            'client_id': self.app_id,
            'scope': self.scope,
            'v': self.v,
        }

    async def authorize(self, num_attempts=1, retry_interval=1):
        log.debug(f'getting authorization page.. {self.OAUTH_URL}')
        url, html = await self._get_auth_page()

        for attempt_num in range(num_attempts):
            if url.path.endswith('authorize') and 'client_id' in url.query:
                log.debug(f'authorizing.. at {url}')
                url, html = await self._process_auth_form(html)

            if url.path.endswith('authorize') and '__q_hash' in url.query:
                log.debug(f'giving rights.. at {url}')
                url, html = await self._process_access_form(html)

            if url.path.endswith('blank.html'):
                log.debug('authorized successfully')
                await self._get_auth_response()
                return self

            if attempt_num >= num_attempts:
                e = AuthError('Authorization failed.')
                raise e

            await asyncio.sleep(retry_interval)
            url, html = await self._get_auth_page()

    async def _get_auth_page(self):
        """Return URL and html code of authorization page."""

        async with self.session.get(self.OAUTH_URL, params=self.params) as resp:
            if resp.status != 200:
                raise AuthError('Wrong "app_id" or "scope".')
            url, html = resp.url, await resp.text()

        return url, html

    async def _process_auth_form(self, html):
        """Submits a form with login and password to get access token.

        Args:
            html (str): authorization page's html code.

        Returns:
            url (URL): redirected page's URL.
            html (str): redirected page's html code.

        """

        parser = AuthPageParser()
        parser.feed(html)
        parser.close()

        form_url, form_data = parser.url, parser.inputs
        form_data['email'] = self.login
        form_data['pass'] = self.passwd

        async with self.session.post(form_url, data=form_data) as resp:
            if resp.status != 200:
                raise AuthError('Failed to process authorization form.')
            url, html = resp.url, await resp.text()

        return url, html

    async def _process_access_form(self, html):
        """Clicks button 'allow' in a page with access form.

        Args:
            html (str): html code of the page with access form.

        Returns:
            url (URL): redirected page's URL.
            html (str): redirected page's html code.

        """

        parser = AccessPageParser()
        parser.feed(html)
        parser.close()

        form_url, form_data = parser.url, parser.inputs

        async with self.session.post(form_url, data=form_data) as resp:
            if resp.status != 200:
                raise AuthError('Failed to process access page.')
            url, html = resp.url, await resp.text()

        return url, html

    async def _get_auth_response(self):
        async with self.session.get(self.OAUTH_URL, params=self.params) as resp:
            location = URL(resp.history[-1].headers['Location'])
            url = URL(f'?{location.fragment}')

        try:
            self.access_token = url.query['access_token']
            self.expires_in = url.query['expires_in']
        except KeyError as e:
            raise AuthError(f'"{e.args[0]}" is missing in the auth response.')
