import aiohttp
import asyncio
import logging

from yarl import URL

from .exceptions import (
    OAuthError,
    InvalidGrantError,
    InvalidUserError,
    APIError,
    EmptyResponseError,
)
from .parsers import AuthPageParser, AccessPageParser


log = logging.getLogger(__name__)


class Session:
    """A wrapper around aiohttp.ClientSession."""

    CONTENT_TYPE = 'application/json; charset=utf-8'

    def __init__(self, pass_error=False, session=None):
        self.pass_error = pass_error
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

    API_URL = 'https://api.vk.com/method/'
    V = '5.101'

    __slots__ = ('access_token', 'v')

    def __init__(self, access_token, v='',
                 pass_error=False, session=None, **kwargs):
        super().__init__(pass_error, session)
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

        url = self.API_URL + '/' + method_name
        params = {k: params[k] for k in params if params[k]}
        params.update(self.required_params)

        async with self.session.get(url, params=params) as resp:
            content = await resp.json(content_type=self.CONTENT_TYPE)

        if self.pass_error:
            response = content
        elif 'error' in content:
            log.error(content)
            raise APIError(content)
        elif content:
            response = content['response']
        else:
            raise EmptyResponseError()

        return response


class CodeSession(TokenSession):
    """Session with authorization with OAuth 2.0 (Authorization Code Grant).

    The Authorization Code grant is used by confidential and public
    clients to exchange an authorization code for an access token.

    .. _OAuth 2.0 Authorization Code Grant
        https://oauth.net/2/grant-types/authorization-code/

    .. _Получение access_token
        https://vk.com/dev/authcode_flow_user?f=4.%20Получение%20access_token

    """

    OAUTH_URL = 'https://oauth.vk.com/access_token'
    GET_ACCESS_TOKEN_ERROR_MSG = 'Failed to receive access token.'

    __slots__ = ('app_id', 'code', 'redirect_uri', 'expires_in', 'user_id')

    def __init__(self, app_id, app_secret, code, redirect_uri, v='',
                 pass_error=False, session=None, **kwargs):
        super().__init__('', v, pass_error, session, **kwargs)
        self.app_id = app_id
        self.app_secret = app_secret
        self.code = code
        self.redirect_uri = redirect_uri

    @property
    def params(self):
        """Authorization request's parameters."""
        return {
            'client_id': self.app_id,
            'client_secret': self.app_secret,
            'redirect_uri': self.redirect_uri,
            'code': self.code,
        }

    async def authorize(self):
        """Authorize with OAuth 2.0 (Authorization Code)."""

        async with self.session.get(self.OAUTH_URL, params=self.params) as resp:
            content = await resp.json(content_type=self.CONTENT_TYPE)

        if 'error' in content:
            log.error(content)
            raise OAuthError(content)
        elif content:
            try:
                self.access_token = content['access_token']
                self.expires_in = content['expires_in']
                self.user_id = content.get('user_id')
            except KeyError as e:
                raise OAuthError('%r is missing in the response' % e.args[0])
        else:
            raise OAuthError('got empty authorization response')

        return self


class ImplicitSession(TokenSession):

    OAUTH_URL = 'https://oauth.vk.com/authorize'
    REDIRECT_URI = 'https://oauth.vk.com/blank.html'

    AUTHORIZE_NUM_ATTEMPTS = 1
    AUTHORIZE_RETRY_INTERVAL = 3

    GET_AUTH_DIALOG_ERROR_MSG = 'Failed to open authorization dialog.'
    POST_AUTH_DIALOG_ERROR_MSG = 'Form submission failed.'
    GET_ACCESS_TOKEN_ERROR_MSG = 'Failed to receive access token.'
    POST_ACCESS_DIALOG_ERROR_MSG = 'Failed to process access dialog.'

    __slots__ = ('app_id', 'login', 'passwd', 'scope',
                 'redirect_uri', 'state', 'revoke', 'expires_in')

    def __init__(self, app_id, login, passwd,
                 scope='', redirect_uri='', state='', revoke=0, v='',
                 pass_error=False, session=None, **kwargs):
        super().__init__('', v, pass_error, session, **kwargs)
        self.app_id = app_id
        self.login = login
        self.passwd = passwd
        self.scope = scope
        self.redirect_uri = redirect_uri or self.REDIRECT_URI
        self.state = state
        self.revoke = revoke

    @property
    def params(self):
        """Authorization request's parameters."""
        return {
            'client_id': self.app_id,
            'redirect_uri': self.redirect_uri,
            'display': 'mobile',
            'scope': self.scope,
            'response_type': 'token',
            'v': self.v,
            'state': self.state,
            'revoke': self.revoke,
        }

    async def authorize(self, num_attempts=None, retry_interval=None):
        """OAuth Implicit flow."""

        num_attempts = num_attempts or self.AUTHORIZE_NUM_ATTEMPTS
        retry_interval = retry_interval or self.AUTHORIZE_RETRY_INTERVAL

        for attempt_num in range(num_attempts):
            log.debug('getting authorization dialog %s' % self.OAUTH_URL)
            url, html = await self._get_auth_dialog()

            if url.path == '/authorize':
                log.debug('authorizing at %s' % url)
                url, html = await self._post_auth_dialog(html)

            if url.path == '/authorize' and '__q_hash' in url.query:
                log.debug('giving rights at %s' % url)
                url, html = await self._post_access_dialog(html)
            elif url.path == '/authorize' and 'email' in url.query:
                log.error('Invalid login "%s" or password.' % self.login)
                raise InvalidGrantError()
            elif url.query.get('act') == 'blocked':
                raise InvalidUserError()

            if url.path == '/blank.html':
                log.debug('authorized successfully')
                await self._get_access_token()
                return self

            await asyncio.sleep(retry_interval)
        else:
            log.error('%d login attempts exceeded.' % num_attempts)
            raise OAuthError('%d login attempts exceeded.' % num_attempts)

    async def _get_auth_dialog(self):
        """Return URL and html code of authorization page."""

        async with self.session.get(self.OAUTH_URL, params=self.params) as resp:
            if resp.status == 401:
                error = await resp.json(content_type=self.CONTENT_TYPE)
                log.error(error)
                raise OAuthError(error)
            elif resp.status != 200:
                log.error(self.GET_AUTH_DIALOG_ERROR_MSG)
                raise OAuthError(self.GET_AUTH_DIALOG_ERROR_MSG)
            else:
                url, html = resp.url, await resp.text()

        return url, html

    async def _post_auth_dialog(self, html):
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

        form_url, form_data = parser.form
        form_data['email'] = self.login
        form_data['pass'] = self.passwd

        async with self.session.post(form_url, data=form_data) as resp:
            if resp.status != 200:
                log.error(self.POST_AUTH_DIALOG_ERROR_MSG)
                raise OAuthError(self.POST_AUTH_DIALOG_ERROR_MSG)
            else:
                url, html = resp.url, await resp.text()

        return url, html

    async def _post_access_dialog(self, html):
        """Clicks button 'allow' in a page with access dialog.

        Args:
            html (str): html code of the page with access form.

        Returns:
            url (URL): redirected page's URL.
            html (str): redirected page's html code.

        """

        parser = AccessPageParser()
        parser.feed(html)
        parser.close()

        form_url, form_data = parser.form

        async with self.session.post(form_url, data=form_data) as resp:
            if resp.status != 200:
                log.error(self.POST_ACCESS_DIALOG_ERROR_MSG)
                raise OAuthError(self.POST_ACCESS_DIALOG_ERROR_MSG)
            else:
                url, html = resp.url, await resp.text()

        return url, html

    async def _get_access_token(self):
        async with self.session.get(self.OAUTH_URL, params=self.params) as resp:
            if resp.status != 200:
                log.error(self.GET_ACCESS_TOKEN_ERROR_MSG)
                raise OAuthError(self.GET_ACCESS_TOKEN_ERROR_MSG)
            else:
                location = URL(resp.history[-1].headers['Location'])
                url = URL('?' + location.fragment)

        try:
            self.access_token = url.query['access_token']
            self.expires_in = url.query['expires_in']
        except KeyError as e:
            raise OAuthError('%r is missing in response.' % e.args[0])
