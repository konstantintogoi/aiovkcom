"""Exceptions."""


class Error(Exception):
    """Base exception."""

    ERROR = 'internal_error'

    @property
    def error(self):
        return self.args[0]

    def __init__(self, error: str or dict):
        arg = error if isinstance(error, dict) else {
            'error': self.ERROR,
            'error_description': error,
        }
        super().__init__(arg)


class OAuthError(Error):
    """OAuth error."""

    ERROR = 'oauth_error'


class CustomOAuthError(Error):
    """Custom errors that raised when authorization failed."""

    ERROR = {'error': '', 'error_description': ''}

    def __init__(self):
        super().__init__(self.ERROR)


class InvalidGrantError(CustomOAuthError):
    """Invalid user credentials."""

    ERROR = {
        'error': 'invalid_grant',
        'error_description': 'invalid login or password',
    }


class InvalidUserError(CustomOAuthError):
    """Invalid user (blocked)."""

    ERROR = {
        'error': 'invalid_user',
        'error_description': 'user is blocked',
    }


class APIError(Error):
    """API error."""

    def __init__(self, error: dict):
        super().__init__(error)
        self.code = error['error'].get('error_code')
        self.msg = error['error'].get('error_msg')
        self.params = error['error'].get('request_params')

    def __str__(self):
        return 'Error {code}: "{msg}". Parameters: {params}.'.format(
            code=self.code, msg=self.msg, params=self.params
        )


class CustomAPIError(APIError):
    """Custom API error."""

    ERROR = {'error': {'error_code': 0, 'error_msg': '', 'request_params': {}}}

    def __init__(self):
        super().__init__(self.ERROR)


class EmptyResponseError(CustomAPIError):
    ERROR = {'error': {
        'error_code': -1, 'error_msg': 'empty response', 'request_params': {}
    }}
