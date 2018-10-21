import contextlib
from functools import wraps
from typing import Callable, Iterator
import base64

import googleapiclient.discovery
import googleapiclient.errors

import google.auth.exceptions

import httplib2

from appsecrets.exc import Error, SecretError, CryptoError
from . import _Crypto


@contextlib.contextmanager
def handle_gcloud_error() -> Iterator[None]:
    try:
        yield
    except googleapiclient.errors.HttpError as err:
        raise SecretError(str(err))
    except google.auth.exceptions.DefaultCredentialsError as err:
        raise Error(str(err))
    except httplib2.ServerNotFoundError as err:
        raise CryptoError(str(err))


class GoogleKMS(_Crypto):

    def __init__(self, key_id: str) -> None:
        self._key_id = key_id
        self._resource_obj = None

    def encrypt(self, plaintext: bytes) -> bytes:
        body = {'plaintext': base64.b64encode(plaintext).decode('ascii')}

        with handle_gcloud_error():
            response = self._api_resource.encrypt(name=self._key_id, body=body).execute()
            payload = response.get('ciphertext')

        if payload is None:
            raise Error('Failed to encrypt secret with Google KMS')

        return base64.b64decode(payload)

    def decrypt(self, ciphertext: bytes) -> bytes:
        body = {'ciphertext': base64.b64encode(ciphertext).decode('ascii')}

        with handle_gcloud_error():
            response = self._api_resource.decrypt(name=self._key_id, body=body).execute()
            payload = response.get('plaintext')

        if payload is None:
            raise Error('Failed to decrypt secret with Google KMS')

        return base64.b64decode(payload)

    @property
    def _api_resource(self) -> googleapiclient.discovery.Resource:
        if self._resource_obj is None:
            client = googleapiclient.discovery.build('cloudkms', 'v1', cache_discovery=False)
            self._resource_obj = client.projects().locations().keyRings().cryptoKeys()
        return self._resource_obj
