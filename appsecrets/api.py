from pathlib import Path
from typing import Sequence

from . import stores
from .exc import Error


class Secrets:

    def __init__(self, path: str) -> None:
        self._path = path
        self._store = stores.build(path)

    @classmethod
    def create(cls, path: str, key_id: str) -> None:
        if Path(path).exists():
            raise Error(f'A secret store already exists at {path}')

        Path(path).mkdir(parents=True)

        key_id_path = Path(path).joinpath('_google_kms_key_id')
        key_id_path.write_text(key_id)  # pylint: disable=no-member

    def encrypt_all(self) -> None:
        """Encrypt all cleartext secrets in place."""
        self._store.encrypt_inplace()

    def decrypt(self, name: str) -> bytes:
        """Decrypt and return a secrets."""
        return self._store.decrypt(name)

    def list_encrypted(self) -> Sequence[str]:
        """List all encrypted secrets."""
        return self._store.list_encrypted()

    def list_unencrypted(self) -> Sequence[str]:
        """List all unencrypted secrets."""
        return self._store.list_unencrypted()

    def __repr__(self) -> str:
        store_type = str(type(self._store))
        return f'Appsecret({store_type}) at {self._path}'
