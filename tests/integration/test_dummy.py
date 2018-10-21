import base64

import pytest

import appsecrets


PLAINTEXT = b'MYSECRET'
CIPHERTEXT = base64.b64encode(b'DUMMY:MYKEY:' + PLAINTEXT)


@pytest.fixture(autouse=True)
def setup(secretsdir):
    secretsdir.join('_dummy_key_id').write('MYKEY')


def test_check_with_no_secrets(secretsdir, cmd):
    cmd.run('check', secretsdir)


def test_check_with_one_plaintext_secret(secretsdir, cmd):
    secretsdir.join('mysecret').write(PLAINTEXT, 'wb')
    cmd.run_with_error('check', secretsdir)


def test_encrypt_with_no_secrets(secretsdir, cmd):
    cmd.run('encrypt', secretsdir)


def test_encrypt(secretsdir, cmd):
    secretsdir.join('mysecret').write(PLAINTEXT, 'wb')

    cmd.run('encrypt', secretsdir)
    assert secretsdir.join('mysecret').check() is False
    assert secretsdir.join('mysecret.enc').check()
    assert secretsdir.join('mysecret.enc').read('rb') == CIPHERTEXT


def test_decrypt(secretsdir, cmd):
    secretsdir.join('mysecret.enc').write(CIPHERTEXT, 'wb')

    output = cmd.run('decrypt', secretsdir, 'mysecret')
    assert output == PLAINTEXT


def test_decrypt_unknown_secret(secretsdir, cmd):
    err = cmd.run_with_error('decrypt', secretsdir, 'not-found')
    assert b"does not exist" in err


def test_api_encrypt_all(secretsdir):
    secretsdir.join('mysecret').write(PLAINTEXT, 'wb')

    appsecrets.Secrets(path=str(secretsdir)).encrypt_all()

    assert secretsdir.join('mysecret').check() is False
    assert secretsdir.join('mysecret.enc').check()
    assert secretsdir.join('mysecret.enc').read('rb') == CIPHERTEXT


def test_api_decrypt(secretsdir, cmd):
    secretsdir.join('mysecret.enc').write(CIPHERTEXT, 'wb')

    value = appsecrets.Secrets(path=str(secretsdir)).decrypt('mysecret')
    assert value == PLAINTEXT
