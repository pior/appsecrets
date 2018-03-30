import subprocess

import httpretty as httpretty_module

import pytest


@pytest.fixture(autouse=True)
def auto_httpretty_setup():
    httpretty_module.enable()
    httpretty_module.HTTPretty.allow_net_connect = False


@pytest.fixture
def httpretty():
    return httpretty_module


class Cmd:
    @classmethod
    def run(cls, *args):
        proc = subprocess.run(['appsecrets', *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert proc.returncode == 0, f'Failed (code={proc.returncode})\nout: {proc.stdout}\nserr: {proc.stderr}'
        return proc.stdout

    @classmethod
    def run_with_error(cls, *args):
        proc = subprocess.run(['appsecrets', *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert proc.returncode == 1, f'Didn\'t fail (code={proc.returncode})\nout: {proc.stdout}\nerr: {proc.stderr}'
        return proc.stderr


@pytest.fixture
def cmd():
    return Cmd


@pytest.fixture
def secretsdir(tmpdir):
    return tmpdir.mkdir('secrets')
