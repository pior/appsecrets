import base64

import googleapiclient.discovery
import googleapiclient.errors

from appsecrets.exc import Error


class GoogleKMS(object):
    def __init__(self, key_id):
        self._key_id = key_id
        self._resource_obj = None

    def encrypt(self, plaintext):
        body = {'plaintext': base64.b64encode(plaintext).decode('ascii')}

        try:
            response = self._api_resource.encrypt(name=self._key_id, body=body).execute()
        except googleapiclient.errors.HttpError as err:
            raise Error(err._get_reason())

        payload = response.get('ciphertext')
        if payload is None:
            raise Error('Failed to encrypt secret with Google KMS')

        return base64.b64decode(payload)

    def decrypt(self, ciphertext):
        body = {'ciphertext': base64.b64encode(ciphertext).decode('ascii')}

        try:
            response = self._api_resource.decrypt(name=self._key_id, body=body).execute()
        except googleapiclient.errors.HttpError as err:
            raise Error(err._get_reason())

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
