# AppSecrets

[![Version](https://img.shields.io/pypi/v/appsecrets.svg)](https://pypi.python.org/pypi/appsecrets)
[![License](https://img.shields.io/pypi/l/appsecrets.svg)](https://pypi.python.org/pypi/appsecrets)
[![PythonVersions](https://img.shields.io/pypi/pyversions/appsecrets.svg)](https://pypi.python.org/pypi/appsecrets)
[![Build](https://travis-ci.org/pior/appsecrets.svg?branch=master)](https://travis-ci.org/pior/appsecrets)

Python 3.6+ library to manage your application secrets with [Google Cloud KMS](https://cloud.google.com/kms/)


## How are my secrets stored?

The secret store currently supported is [Google Cloud KMS](https://cloud.google.com/kms/).
Other secret stores (like [EJSON](https://github.com/Shopify/ejson) or [AWS KMS](https://aws.amazon.com/kms/)) may
be added (contributions are welcome).

### Google KMS

Google KMS is a service that manage encryption keys for you. It also offer API calls to encrypt/decrypt arbitrary
payloads with those keys. The Google KMS key is identified by a "resource id".

The secret store is a directory composed of:

- a special file to store the key id (`_google_kms_key_id`)
- files containing plaintext secrets
- files containing encrypted secrets with an `.enc` extension
- files prefixed with `_`, never encrypted


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

Initialize the secret store:
```bash
$ appsecrets create secrets/production --google-kms projects/project-1/locations/global/keyRings/keyring1/cryptoKeys/key1
```

Or manually:
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


## Development

PyReleaser uses [pior/Dad](https://github.com/pior/dad).

If you don't want to use *Dad*, take a look at the file `dev.yml` to know how the project
is setup/linted/tested/released.

- Install [pior/Dad](https://github.com/pior/dad#install)
- Run `dad up` to setup the development environment

Create a new release:
```
$ dad release 0.4.0
```

Publish the release:
```
$ dad publish
```
