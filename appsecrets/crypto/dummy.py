
class Dummy(object):
    _MARKER = b'DUMMY'

    def __init__(self, key_id):
        self._key_id_as_bytes = bytes(key_id, 'utf-8')

    def encrypt(self, plaintext):
        return b':'.join([self._MARKER, self._key_id_as_bytes, plaintext])

    def decrypt(self, ciphertext):
        marker, key_id, rest = ciphertext.split(b':', 2)
        if marker != self._MARKER:
            raise ValueError('Invalid ciphertext (marker not DUMMY)')
        if key_id != self._key_id_as_bytes:
            raise ValueError('Ciphertext doesn\'t match the key_id')
        return rest
