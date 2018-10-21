from base64 import b64decode
import binascii
import os
from typing import Optional

import nacl.public

from . import _Crypto


class EJSON(_Crypto):

    _DEFAULT_PRIVATE_KEY_DIR = '/opt/ejson/keys'

    _VALID_HEADER = b'EJ[1'  # https://github.com/Shopify/ejson/blob/master/crypto/boxed_message.go

    def __init__(self, public_key: str) -> None:
        self._public_key = public_key
        self._private_key_dir = os.environ.get('EJSON_KEYDIR') or self._DEFAULT_PRIVATE_KEY_DIR
        self._private_key: Optional[bytes] = None

    def encrypt(self, plaintext: bytes) -> bytes:
        raise NotImplementedError("Encrypting secrets in ejson is not supported")

    def decrypt(self, ciphertext: bytes) -> bytes:
        header, b64_encpub, b64_nonce, b64_box = ciphertext.split(b':')
        if header != self._VALID_HEADER:
            raise ValueError(f'invalid header EJSON cypher "{header}", only supporting "{self._VALID_HEADER}"')
        encpub = b64decode(b64_encpub)
        nonce = b64decode(b64_nonce)
        box = b64decode(b64_box)
        b = nacl.public.Box(nacl.public.PrivateKey(self._get_private_key()), nacl.public.PublicKey(encpub))
        return b.decrypt(box, nonce)  # type: ignore

    def _get_private_key(self) -> bytes:
        if self._private_key is None:
            self._private_key = self._load_private_key()
        return self._private_key

    def _load_private_key(self) -> bytes:
        path = os.path.join(self._private_key_dir, self._public_key)
        with open(path) as fh:
            data = fh.read()
        private_key = binascii.unhexlify(data.strip())
        if len(private_key) != 32:
            raise IOError('invalid private key')
        return private_key
