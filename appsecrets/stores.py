import abc
import base64
import json
from pathlib import Path
from typing import Sequence

from .crypto import _Crypto
from .crypto.google_kms import GoogleKMS
from .crypto.dummy import Dummy
from .exc import Error, SecretError


class SecretNotFound(Error):

    def __init__(self, name: str) -> None:
        super().__init__(f'Secret "{name}": not found')


class _Store(abc.ABC):

    @abc.abstractmethod
    def encrypt_inplace(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def decrypt(self, name: str) -> bytes:
        raise NotImplementedError()

    @abc.abstractmethod
    def list_encrypted(self) -> Sequence[str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def list_unencrypted(self) -> Sequence[str]:
        raise NotImplementedError()


def build(path: str) -> _Store:
    if not Path(path).exists():
        raise Error("The specified path doesn't exist: %s" % path)

    if not Path(path).is_dir():
        raise Error("The only supported secret store is a directory")
    return DirStore(path)


class DirStore(_Store):
    def __init__(self, path: str) -> None:
        self._path = path
        self._crypto = self._load_crypto()

    def encrypt_inplace(self) -> None:
        for name in self.list_unencrypted():
            plaintext = self._unencrypted_secret_file(name).read_bytes()

            try:
                ciphertext = self._crypto.encrypt(plaintext)
            except SecretError as err:
                raise Error(f'Secret "{name}": {err}')

            self._write_cipher(name, ciphertext)
            self._unencrypted_secret_file(name).unlink()

    def decrypt(self, name: str) -> bytes:
        try:
            return self._crypto.decrypt(self._read_cipher(name))
        except SecretError as err:
            raise Error(f'Secret "{name}": {err}')

    def list_encrypted(self) -> Sequence[str]:
        return [name for name in self._list_names() if name.endswith('.enc')]

    def list_unencrypted(self) -> Sequence[str]:
        return [name for name in self._list_names() if not name.endswith('.enc')]

    def _load_crypto(self) -> _Crypto:
        try:
            return GoogleKMS(key_id=self._read_key_id('google_kms'))
        except FileNotFoundError:
            pass

        try:
            return Dummy(key_id=self._read_key_id('dummy'))
        except FileNotFoundError:
            pass

        raise Error("Missing key file")

    def _read_key_id(self, crypto_id: str) -> str:
        return Path(self._path).joinpath(f'_{crypto_id}_key_id').read_text()

    def _list_names(self) -> Sequence[str]:
        return [entry.name for entry in Path(self._path).iterdir() if not entry.name.startswith('_')]

    def _read_cipher(self, name: str) -> bytes:
        try:
           serialized = self._encrypted_secret_file(name).read_bytes()
        except FileNotFoundError:
            raise SecretError(f'Secret {name} does not exist, or is not encrypted yet')

        return base64.b64decode(serialized)

    def _write_cipher(self, name: str, content: bytes) -> None:
        serialized = base64.b64encode(content)
        self._encrypted_secret_file(name).write_bytes(serialized)

    def _unencrypted_secret_file(self, name: str) -> Path:
        return Path(self._path).joinpath(name)

    def _encrypted_secret_file(self, name: str) -> Path:
        return Path(self._path).joinpath(name + '.enc')



