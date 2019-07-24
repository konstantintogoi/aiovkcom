from . import api, exceptions, parsers, sessions
from .exceptions import AuthError, VKAuthError, VKAPIError
from .sessions import TokenSession, ImplicitSession
from .api import API

import logging


logging.basicConfig()
