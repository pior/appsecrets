import base64
import os.path

import pytest


def has_gcloud_creds():
    adc = '~/.config/gcloud/application_default_credentials.json'
    return os.path.exists(os.path.expanduser(adc))

skipmodule = pytest.mark.skipif(not has_gcloud_creds(), reason='No Gcloud creds')



TEST_KEY_ID = 'projects/pior-secrets/locations/global/keyRings/appsecrets/cryptoKeys/appsecrets-integration-test'


@pytest.fixture(autouse=True)
def setup(secretsdir):
    secretsdir.join('_google_kms_key_id').write(TEST_KEY_ID)


def test_decrypt_invalid_secret(secretsdir, cmd):
    secretsdir.join('mysecret.enc').write(base64.b64encode(b'InvalidKMSData'))
    err = cmd.run_with_error('decrypt', secretsdir, 'mysecret')
    assert b'invalid' in err


def test_encrypt_too_large_secret(secretsdir, cmd):
    b64_value = base64.b64encode(bytes(64 * 1024))
    assert len(b64_value) > 64 * 1024

    secretsdir.join('mysecret').write(b64_value)

    err = cmd.run_with_error('encrypt', secretsdir)
    assert b'but not more than 65536' in err
