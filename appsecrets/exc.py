class Error(Exception):
    """Generic error about appsecrets."""
    pass


class SecretError(Error):
    """Error likely to be specific to a single secret."""
    pass


class CryptoError(Error):
    """Error produced by a crypto backend."""
    pass
