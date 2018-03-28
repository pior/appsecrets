import subprocess

import pytest

import appsecrets


@pytest.fixture()
def secretsdir(tmpdir):
    return tmpdir.mkdir('secrets')


@pytest.fixture(autouse=True)
def setup(secretsdir):
    secretsdir.join('_dummy_key_id').write('MYKEY')
    secretsdir.join('secret1').write('MYSECRET')


def test_cli(secretsdir):
    process = subprocess.run(['appsecrets', 'check', secretsdir])
    assert process.returncode == 1

    process = subprocess.run(['appsecrets', 'encrypt', secretsdir])
    assert process.returncode == 0

    process = subprocess.run(['appsecrets', 'check', secretsdir])
    assert process.returncode == 0

    process = subprocess.run(['appsecrets', 'decrypt', secretsdir, 'secret1'], stdout=subprocess.PIPE)
    assert process.stdout == b'MYSECRET'


def test_api(secretsdir):
    process = subprocess.run(['appsecrets', 'encrypt', secretsdir])
    assert process.returncode == 0

    secrets = appsecrets.Secrets(path=str(secretsdir))
    plaintext = secrets.decrypt('secret1')

    assert plaintext == b'MYSECRET'
