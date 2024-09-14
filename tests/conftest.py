"""Conftest."""
import json
from asyncio import AbstractEventLoop, get_event_loop_policy
from typing import Any, Dict, Generator

import pytest


@pytest.fixture(scope='session')
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    """Event loop."""
    loop = get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def error_response() -> Dict[str, Any]:
    """Return an error."""
    return {'error': {
        'error_code': -1,
        'error_msg': 'test error msg',
        'request_params': {},
    }}


@pytest.fixture
def data_response() -> Dict[str, Any]:
    """Return data."""
    return {'response': {'key': 'value'}}


@pytest.fixture
async def error_server(httpserver, error_response):
    """Return a server with error response."""
    httpserver.serve_content(**{
        'code': 401,
        'headers': {'Content-Type': 'application/json; charset=utf-8'},
        'content': json.dumps(error_response),
    })
    return httpserver


@pytest.fixture
async def data_server(httpserver, data_response):
    """Return a server with regular response."""
    httpserver.serve_content(**{
        'code': 200,
        'headers': {'Content-Type': 'application/json; charset=utf-8'},
        'content': json.dumps(data_response),
    })
    return httpserver
