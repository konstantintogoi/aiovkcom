import json

import pytest

from aiovkcom import OAuthError, APIError, EmptyResponseError
from aiovkcom.sessions import TokenSession, ImplicitSession


class TestTokenSession:
    """Tests of TokenSession class."""

    @pytest.fixture
    def token(self):
        return {'access_token': ''}

    @pytest.mark.asyncio
    async def test_required_params(self, token):
        async with TokenSession(**token) as session:
            assert 'v' in session.required_params
            assert 'access_token' in session.required_params

    @pytest.mark.asyncio
    async def test_error_request(self, token, error_server, error):
        async with TokenSession(**token) as session:
            session.API_URL = error_server.url

            session.pass_error = True
            response = await session.request('', params={'key': 'value'})
            assert response == error

    @pytest.mark.asyncio
    async def test_error_request_with_raising(self, token, error_server):
        async with TokenSession(**token) as session:
            session.API_URL = error_server.url

            session.pass_error = False
            with pytest.raises(APIError):
                await session.request('', params={'key': 'value'})

    @pytest.mark.asyncio
    async def test_dummy_request(self, token, dummy_server, dummy):
        async with TokenSession(**token) as session:
            session.API_URL = dummy_server.url

            session.pass_error = True
            response = await session.request('', params={'key': 'value'})
            assert response == dummy

    @pytest.mark.asyncio
    async def test_dummy_request_with_raising(self, token, dummy_server):
        async with TokenSession(**token) as session:
            session.API_URL = dummy_server.url

            session.pass_error = False
            with pytest.raises(EmptyResponseError):
                await session.request('', params={'key': 'value'})

    @pytest.mark.asyncio
    async def test_data_request(self, token, data_server, data):
        async with TokenSession(**token) as session:
            session.API_URL = data_server.url

            session.pass_error = True
            response = await session.request('', params={'key': 'value'})
            assert response == data

            session.pass_error = False
            response = await session.request('', params={'key': 'value'})
            assert response == data['response']


class TestImplicitSession:
    """Tests of ImplicitSession class."""

    @pytest.fixture
    def app(self):
        return {'app_id': 123}

    @pytest.fixture
    def cred(self):
        return {
            'login': 'email@example.ru',
            'passwd': 'password',
            'scope': 'permission1 permission2 permission3',
        }

    @pytest.mark.asyncio
    async def test_get_auth_dialog(self, app, cred, httpserver, auth_dialog):
        # success
        httpserver.serve_content(**{
            'code': 200,
            'headers': {'Content-Type': 'text/html'},
            'content': auth_dialog,
        })
        session = ImplicitSession(**app, **cred)
        session.OAUTH_URL = httpserver.url
        url, html = await session._get_auth_dialog()

        assert url.query['display'] == session.params['display']
        assert url.query['response_type'] == session.params['response_type']
        assert url.query['redirect_uri'] == session.REDIRECT_URI
        assert url.query['client_id'] == str(session.app_id)
        assert url.query['scope'] == session.scope
        assert html == auth_dialog

        # fail
        httpserver.serve_content(**{
            'code': 400,
            'headers': {'Content-Type': 'text/json'},
            'content': json.dumps({'error': '', 'error_description': ''})
        })
        with pytest.raises(OAuthError):
            _ = await session._get_auth_dialog()

        await session.close()

    @pytest.mark.asyncio
    async def test_post_auth_dialog(self, app, cred, httpserver,
                                    auth_dialog, access_dialog):
        # success
        httpserver.serve_content(**{'code': 200, 'content': access_dialog})
        session = ImplicitSession(**app, **cred)

        auth_dialog = auth_dialog.replace(
            'https://login.vk.com/?act=login&soft=1', httpserver.url,
        )
        url, html = await session._post_auth_dialog(auth_dialog)
        assert html == access_dialog

        # fail
        httpserver.serve_content(**{'code': 400, 'content': ''})
        with pytest.raises(OAuthError):
            _ = await session._post_auth_dialog(auth_dialog)

        await session.close()

    @pytest.mark.asyncio
    async def test_post_access_dialog(self, app, cred, httpserver, access_dialog):
        # success
        httpserver.serve_content(**{'code': 200, 'content': 'blank page'})
        session = ImplicitSession(**app, **cred)

        access_dialog = access_dialog.replace(
            'https://login.vk.com/?act=grant_access', httpserver.url
        )
        url, html = await session._post_access_dialog(access_dialog)
        assert html == 'blank page'

        # fail
        httpserver.serve_content(**{'code': 400, 'content': ''})
        with pytest.raises(OAuthError):
            _ = await session._post_access_dialog(access_dialog)

        await session.close()

    @pytest.mark.asyncio
    async def test_get_access_token(self, app, cred, httpserver):
        # fail
        httpserver.serve_content(**{'code': 400, 'content': ''})
        session = ImplicitSession(**app, **cred)
        session.OAUTH_URL = httpserver.url

        with pytest.raises(OAuthError):
            _ = await session._get_access_token()

        await session.close()
