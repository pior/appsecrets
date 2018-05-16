import socket

import pytest

from appsecrets.exc import Error, CryptoError
from appsecrets.crypto.google_kms import GoogleKMS


def test_encrypt(mocker):
    mocker.patch.object(GoogleKMS, '_api_resource')
    GoogleKMS._api_resource.encrypt.return_value.execute.return_value = {'ciphertext': 'Q0lQSEVS'}

    enc = GoogleKMS('testkeyid').encrypt(b'PLAIN')
    assert enc == b'CIPHER'


def test_encrypt_failed(mocker):
    mocker.patch.object(GoogleKMS, '_api_resource')
    GoogleKMS._api_resource.encrypt.return_value.execute.return_value = {}

    with pytest.raises(Error):
        GoogleKMS('testkeyid').encrypt(b'PLAIN')


def test_decrypt(mocker):
    mocker.patch.object(GoogleKMS, '_api_resource')
    GoogleKMS._api_resource.decrypt.return_value.execute.return_value = {'plaintext': 'UExBSU4='}

    enc = GoogleKMS('testkeyid').decrypt(b'CIPHER')
    assert enc == b'PLAIN'


def test_decrypt_failed(mocker):
    mocker.patch.object(GoogleKMS, '_api_resource')
    GoogleKMS._api_resource.decrypt.return_value.execute.return_value = {}

    with pytest.raises(Error):
        GoogleKMS('testkeyid').decrypt(b'CIPHER')


def test_network_error(mocker):
    m_socket = mocker.patch('socket.socket', autospec=True)
    m_socket.side_effect = socket.gaierror('TEST')

    with pytest.raises(CryptoError) as exc_info:
        GoogleKMS('testkeyid').decrypt(b'CIPHER')

    assert str(exc_info.value) == 'Unable to find the server at www.googleapis.com'
