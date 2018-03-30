def test_create(tmpdir, cmd):
    secretsdir = tmpdir.join('secrets')

    cmd.run('create', secretsdir, '--google-kms', 'KEY-ID')

    assert secretsdir.check()
    assert secretsdir.join('_google_kms_key_id').read() == 'KEY-ID'


def test_create_already_exists(secretsdir, cmd):
    err = cmd.run_with_error('create', secretsdir, '--google-kms', 'KEY-ID')
    assert b'secret store already exists' in err
