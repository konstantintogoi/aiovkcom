class Error(Exception):
    pass


class AuthError(Error):
    pass


class APIError(Error):
    def __init__(self, error, *args):
        super().__init__(error, *args)
        self.code = error['error_code']
        self.msg = error['error_msg']
        self.params = error['request_params']

    def __str__(self):
        return f'Error {self.code}: {self.msg}. Parameters: {self.params}'
