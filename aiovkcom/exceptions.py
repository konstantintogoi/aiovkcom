class Error(Exception):
    pass


class AuthError(Error):
    pass


class VKAuthError(Error):
    def __init__(self, error: dict, *args):
        super().__init__(error, *args)

    def __getitem__(self, item):
        return self.args[0].__getitem__(item)


class VKAPIError(Error):
    def __init__(self, error: dict, *args):
        super().__init__(error, *args)

    def __getitem__(self, item):
        return self.args[0].__getitem__(item)

    def __str__(self):
        return (f'Error {self["error_code"]}: {self["error_msg"]}. '
                f'Parameters: {self["request_params"]}')
