from . import api, exceptions, parsers, sessions
from .exceptions import AuthError, APIError
from .sessions import TokenSession, ImplicitSession
from .api import API

import logging


logging.basicConfig()
