from pathlib import Path
from typing import Sequence

from . import stores
from .exc import Error, SecretNotFound


class Secrets:

    """Encrypt and decrypt secrets.

    The secrets location is specified by the `path` argument.

    In test mode (`test_mode` argument), the decryption of an existing and
    encrypted secret will always succeed and return a dummy value, without
    actually decrypting the secret. If the secret does not exist,
    SecretNotFound will be raise. It can be useful to test that an application
    only access existing secrets.
    """

    def __init__(self, path: str, test_mode: bool = False) -> None:
        self._path = path
        self._store = stores.build(path)
        self._test_mode = test_mode

    @classmethod
    def create(cls, path: str, key_id: str) -> None:
        if Path(path).exists():
            raise Error(f'A secret store already exists at {path}')

        Path(path).mkdir(parents=True)

        key_id_path = Path(path).joinpath('_google_kms_key_id')
        key_id_path.write_text(key_id)  # pylint: disable=no-member

    def encrypt_all(self) -> None:
        """Encrypt all cleartext secrets in place."""

        if self._test_mode:
            raise Error('Can not encrypt secrets in test-mode')

        self._store.encrypt_inplace()

    def decrypt(self, name: str) -> bytes:
        """Decrypt and return a secrets."""
        if self._test_mode:
            if name in self._store.list_encrypted():
                return b'test-mode-' + bytes(name, 'utf-8')
            raise SecretNotFound(name)

        return self._store.decrypt(name)

    def list_encrypted(self) -> Sequence[str]:
        """List all encrypted secrets."""
        return self._store.list_encrypted()

    def list_unencrypted(self) -> Sequence[str]:
        """List all unencrypted secrets."""
        return self._store.list_unencrypted()

    def __repr__(self) -> str:
        return f'Secrets({self._path!r})'
