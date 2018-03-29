from . import stores


class Secrets(object):
    def __init__(self, path):
        self._store = stores.build(path)

    def encrypt_all(self):
        """Encrypt all cleartext secrets in place."""
        self._store.encrypt_inplace()

    def decrypt(self, name):
        """Decrypt and return a secrets."""
        return self._store.decrypt(name)

    def list_encrypted(self):
        """List all encrypted secrets."""
        return self._store.list_encrypted()

    def list_unencrypted(self):
        """List all unencrypted secrets."""
        return self._store.list_unencrypted()
