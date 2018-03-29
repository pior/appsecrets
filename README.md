# AppSecrets

[![Version](https://img.shields.io/pypi/v/appsecrets.svg)](https://pypi.python.org/pypi/appsecrets)
[![License](https://img.shields.io/pypi/l/appsecrets.svg)](https://pypi.python.org/pypi/appsecrets)
[![PythonVersions](https://img.shields.io/pypi/pyversions/appsecrets.svg)](https://pypi.python.org/pypi/appsecrets)
[![Build](https://travis-ci.org/pior/appsecrets.svg?branch=master)](https://travis-ci.org/pior/appsecrets)

Python 3.6+ library to manage your application secrets with [Google Cloud KMS](https://cloud.google.com/kms/)


## Usage

```shell
$ pip install appsecrets
...
```

**Python API**

```python
import appsecrets

secrets = appsecrets.Secrets('secrets/production')
plaintext = secrets.decrypt('secret1')
```

**Command line**

```bash
$ mkdir -p secrets/production
$ echo 'projects/project-1/locations/global/keyRings/keyring1/cryptoKeys/key1' > secrets/production/_google_kms_key_id
$ echo 'MYSECRET' > secrets/production/secret1
```

Check that all secrets are encrypted:
```bash
$ appsecrets check secrets/production
```

Encrypt all the plaintext secrets:
```bash
$ appsecrets encrypt secrets/production
```

Decrypt a single secret:
```bash
$ appsecrets decrypt secrets/production secret1
```
