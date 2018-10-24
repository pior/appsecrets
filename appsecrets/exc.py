class Error(Exception):
    """Generic error about appsecrets."""
    pass


class SecretError(Error):
    """Error likely to be specific to a single secret."""
    pass


class SecretNotFound(SecretError):

    def __init__(self, name: str) -> None:
        super().__init__(f'Secret "{name}": not found')


class CryptoError(Error):
    """Error produced by a crypto backend."""
    pass
