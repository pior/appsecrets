import base64

import pytest

import appsecrets


TEST_PRIV = 'ccf94c1cc911ec62994ba53ba728379a307f584c33d1061b9872c7aad5754326'
TEST_PUB = 'b8f6821146674779489adb3ce1397f979eaf5d7ae2c891d74267190641c9e10b'

TEST_EJSON_FILE = '''
{
  "_public_key": "b8f6821146674779489adb3ce1397f979eaf5d7ae2c891d74267190641c9e10b",
  "_not_encrypted": "NOT_SECRET",
  "encrypted": "EJ[1:uwAKLP3KaYiKfKNjZ+bWMEgJwMoBKi91WJzLSfMBo3w=:Q+GtbFj6gQogN2BXybi1kw3sWOdvAtpC:sEJ+i1BE8GZTuk4sjIFOcsSE/kyHkw==]",
  "with_space": "EJ[1:uwAKLP3KaYiKfKNjZ+bWMEgJwMoBKi91WJzLSfMBo3w=:/G/9ZZhFld8yLUA5uxdLmkM6xrP40EP+:DKEmNj/xPBs4309bnnEJ8pbizpALTyOn]",
  "nested": {
  	"encrypted": "EJ[1:uwAKLP3KaYiKfKNjZ+bWMEgJwMoBKi91WJzLSfMBo3w=:L3hid20srRC6zHL3zxt5Z4q7U31CHFcW:axvgi39VBYVS2oLJS76ihjtn2whXzA==]"
  }
}
'''

@pytest.fixture
def ejsonfile(secretsdir):
    f = secretsdir.join('somefile.ejson')
    f.write(TEST_EJSON_FILE)
    return f


@pytest.fixture(autouse=True)
def setup_keydir(tmpdir, secretsdir, ejsonfile, monkeypatch):
    ejson_keydir = tmpdir.mkdir('ejson_keydir')
    ejson_keydir.join(TEST_PUB).write(TEST_PRIV)
    monkeypatch.setenv('EJSON_KEYDIR', str(ejson_keydir))


def test_encrypt(secretsdir, ejsonfile, cmd):
    value = appsecrets.Secrets(path=str(ejsonfile)).decrypt('encrypted')
    assert value == 'SECRET'


def test_decrypt(secretsdir, ejsonfile, cmd):
    value = appsecrets.Secrets(path=str(ejsonfile)).decrypt('encrypted')
    assert value == 'SECRET'


def test_file_not_found(secretsdir, cmd):
    with pytest.raises(appsecrets.exc.Error) as exc:
        appsecrets.Secrets(path=str(secretsdir.join('nofile.ejson')))
    assert "The specified path doesn't exist" in str(exc.value)
