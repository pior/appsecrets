import pytest

import appsecrets
import appsecrets.exc


@pytest.fixture(autouse=True)
def setup(secretsdir):
    secretsdir.join('_dummy_key_id').write('DUMMYKEY')


def test_empty_dir_store(tmpdir):
    with pytest.raises(appsecrets.exc.Error) as exc:
        appsecrets.Secrets(str(tmpdir))
    assert 'Missing key file' in str(exc.value)


def test_nonexistant_path(tmpdir):
    with pytest.raises(appsecrets.exc.Error) as exc:
        appsecrets.Secrets(str(tmpdir.join('nope')))
    assert "The specified path doesn't exist" in str(exc.value)


def test_repr(secretsdir):
    secrets = appsecrets.Secrets(str(secretsdir))
    assert f"Secrets('{secretsdir}')" in repr(secrets)


def test_list_secrets(secretsdir):
    secretsdir.join('sec1.enc').write(b'')
    secretsdir.join('sec2.enc').write(b'')
    secretsdir.join('sec3').write(b'')

    secrets = appsecrets.Secrets(str(secretsdir))

    result = secrets.list_encrypted()
    assert set(result) == set(['sec1', 'sec2'])

    result = secrets.list_unencrypted()
    assert result == ['sec3']


def test_encrypt(secretsdir, cmd):
    secretsdir.join('sec1').write(b'TESTTESTTEST')

    secrets = appsecrets.Secrets(str(secretsdir))
    secrets.encrypt_all()

    assert not secretsdir.join('sec1').exists()
    assert secretsdir.join('sec1.enc').exists()
    assert secretsdir.join('sec1.enc').read() == 'RFVNTVk6RFVNTVlLRVk6VEVTVFRFU1RURVNU'  # base64


@pytest.mark.parametrize("test_value", [b'testtest', b' testtest ', b'', b'\xFF\xFF'])
def test_decrypt(secretsdir, cmd, test_value):
    secretsdir.join('sec1').write_binary(test_value)

    secrets = appsecrets.Secrets(str(secretsdir))
    secrets.encrypt_all()

    decrypted = secrets.decrypt('sec1')
    assert decrypted == test_value
