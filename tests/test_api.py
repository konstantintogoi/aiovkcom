"""Session tests."""
import pytest
from httpx import HTTPStatusError

from aiovkcom.api import API


class TestTokenSession:
    """Tests of TokenSession class."""

    @pytest.mark.asyncio
    async def test_error_response(self, error_server):
        """Test request with error response."""
        async with API(v='', access_token='') as api:
            api.session.client.base_url = error_server.url

            with pytest.raises(HTTPStatusError):
                await api.friends.get()

    @pytest.mark.asyncio
    async def test_data_response(self, data_server, data_response):
        """Test request with regular response."""
        async with API(v='', access_token='') as api:
            api.session.client.base_url = data_server.url

            assert (await api.friends.get()) == data_response
