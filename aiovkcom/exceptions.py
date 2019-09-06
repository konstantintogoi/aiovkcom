class Error(Exception):

    @property
    def error(self):
        return self.args[0]

    def __init__(self, error: str or dict):
        arg = error if isinstance(error, dict) else {
            'error': 'internal_error',
            'error_description': error,
        }
        super().__init__(arg)


class OAuthError(Error):
    """OAuth error."""

    def __init__(self, error: str):
        super().__init__({'error': 'oauth_error', 'error_description': error})


class VKOAuthError(Error):
    """Invalid client id."""

    def __init__(self, error: dict):
        super().__init__(error)


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


class VKAPIError(Error):
    def __init__(self, error: dict):
        super().__init__(error)

    def __str__(self):
        return (f'Error {self.error["error_code"]}: '
                f'{self.error["error_msg"]} '
                f'Parameters: {self.error["request_params"]}')
