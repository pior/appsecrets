import base64
import os.path

from .crypto.google_kms import GoogleKMS
from .crypto.dummy import Dummy
from .exc import Error


def build(path):
    if not os.path.exists(path):
        raise Error("The specified path doesn't exist: %s" % path)

    if not os.path.isdir(path):
        raise Error("The only supported secret store is a directory")
    return DirStore(path)


class DirStore(object):
    def __init__(self, path):
        self._path = path
        self._crypto = self._load_crypto()

    def encrypt_inplace(self):
        for name in self.list_unencrypted():
            plaintext = self._read_plain(name)
            ciphertext = self._crypto.encrypt(plaintext)
            self._write_cipher(name, ciphertext)
            self._delete_plaintext(name)

    def decrypt(self, name):
        return self._crypto.decrypt(self._read_cipher(name))

    def list_encrypted(self):
        return [name for name in self._list_names() if name.endswith('.enc')]

    def list_unencrypted(self):
        return [name for name in self._list_names() if not name.endswith('.enc')]

    def _load_crypto(self):
        try:
            return GoogleKMS(key_id=self._read_key_id('google_kms'))
        except FileNotFoundError:
            pass

        try:
            return Dummy(key_id=self._read_key_id('dummy'))
        except FileNotFoundError:
            pass

        raise Error("Missing key file")

    def _read_key_id(self, type):
        with open(os.path.join(self._path, '_%s_key_id' % type)) as fh:
            return fh.read().strip()

    def _list_names(self):
        return [name for name in os.listdir(self._path) if not name.startswith('_')]

    def _read_cipher(self, name):
        with open(os.path.join(self._path, name + '.enc'), 'rb') as fh:
            serialized = fh.read()
        return base64.b64decode(serialized)

    def _write_cipher(self, name, content):
        serialized = base64.b64encode(content)
        with open(os.path.join(self._path, name + '.enc'), 'wb') as fh:
            fh.write(serialized)

    def _read_plain(self, name):
        with open(os.path.join(self._path, name), 'rb') as fh:
            return fh.read()

    def _delete_plaintext(self, name):
        os.unlink(os.path.join(self._path, name))
