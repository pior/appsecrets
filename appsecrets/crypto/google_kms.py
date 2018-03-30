from functools import wraps
import base64

import googleapiclient.discovery
import googleapiclient.errors

import oauth2client.client

from appsecrets.exc import Error, SecretError


def handle_gcloud_error(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        try:
            return func(*args, **kwds)
        except googleapiclient.errors.HttpError as err:
            raise SecretError(err._get_reason())
        except oauth2client.client.ApplicationDefaultCredentialsError as err:
            raise Error(str(err))
    return wrapper


class GoogleKMS(object):
    def __init__(self, key_id):
        self._key_id = key_id
        self._resource_obj = None

    @handle_gcloud_error
    def encrypt(self, plaintext):
        body = {'plaintext': base64.b64encode(plaintext).decode('ascii')}

        response = self._api_resource.encrypt(name=self._key_id, body=body).execute()
        payload = response.get('ciphertext')

        if payload is None:
            raise Error('Failed to encrypt secret with Google KMS')

        return base64.b64decode(payload)

    @handle_gcloud_error
    def decrypt(self, ciphertext):
        body = {'ciphertext': base64.b64encode(ciphertext).decode('ascii')}

        response = self._api_resource.decrypt(name=self._key_id, body=body).execute()
        payload = response.get('plaintext')

        if payload is None:
            raise Error('Failed to decrypt secret with Google KMS')

        return base64.b64decode(payload)

    @property
    def _api_resource(self):
        if self._resource_obj is None:
            client = googleapiclient.discovery.build('cloudkms', 'v1')
            self._resource_obj = client.projects().locations().keyRings().cryptoKeys()
        return self._resource_obj
