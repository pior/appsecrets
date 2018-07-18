import base64
import os.path

import pytest


def has_gcloud_creds():
    adc = '~/.config/gcloud/application_default_credentials.json'
    return os.path.exists(os.path.expanduser(adc))


with_gcloud = pytest.mark.skipif(not has_gcloud_creds(), reason='Only with Gcloud creds')
without_gcloud = pytest.mark.skipif(has_gcloud_creds(), reason='Only without Gcloud creds')


TEST_KEY_ID = 'projects/pior-secrets/locations/global/keyRings/appsecrets/cryptoKeys/appsecrets-integration-test'


@pytest.fixture(autouse=True)
def setup(secretsdir):
    secretsdir.join('_google_kms_key_id').write(TEST_KEY_ID)


@with_gcloud
def test_decrypt_invalid_secret(secretsdir, cmd):
    secretsdir.join('mysecret.enc').write(base64.b64encode(b'InvalidKMSData'))
    err = cmd.run_with_error('decrypt', secretsdir, 'mysecret')
    assert 'Secret "mysecret"' in str(err)
    assert 'Decryption failed: the ciphertext is invalid.' in str(err)


@with_gcloud
def test_encrypt_too_large_secret(secretsdir, cmd):
    b64_value = base64.b64encode(bytes(64 * 1024))
    assert len(b64_value) > 64 * 1024

    secretsdir.join('mysecret').write(b64_value)

    err = cmd.run_with_error('encrypt', secretsdir)
    assert b'but not more than 65536' in err


@without_gcloud
def test_without_gcloud_credentials(secretsdir, cmd):
    secretsdir.join('mysecret').write(b'whatever')

    err = cmd.run_with_error('encrypt', secretsdir)
    assert b'Could not automatically determine credentials.' in err
