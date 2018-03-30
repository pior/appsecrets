import pathlib

from . import stores
from .exc import Error


class Secrets(object):
    def __init__(self, path):
        self._path = path
        self._store = stores.build(path)

    @classmethod
    def create(self, path, key_id):
        path = pathlib.Path(path)
        if path.exists():
            raise Error(f'A secret store already exists at {path}')

        path.mkdir(parents=True)

        key_id_path = path.joinpath('_google_kms_key_id')
        key_id_path.write_text(key_id)

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

    def __repr__(self):
        return f'Appsecret({type(self._store)}) at {self._path}'
