import abc


class _Crypto(abc.ABC):

    @abc.abstractmethod
    def encrypt(self, plaintext: bytes) -> bytes:
        raise NotImplementedError()

    @abc.abstractmethod
    def decrypt(self, ciphertext: bytes) -> bytes:
        raise NotImplementedError()
