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


class AuthError(Error):

    ERROR = {
        'error': 'invalid_user_credentials',
        'error_description': 'invalid login or password',
    }

    def __init__(self):
        super().__init__(self.ERROR)


class VKAuthError(Error):
    """Error 401. Invalid 'client_id'."""

    def __init__(self, error: dict):
        super().__init__(error)


class VKAPIError(Error):
    def __init__(self, error: dict):
        super().__init__(error)

    def __str__(self):
        return (f'Error {self.error["error_code"]}: '
                f'{self.error["error_msg"]} '
                f'Parameters: {self.error["request_params"]}')
