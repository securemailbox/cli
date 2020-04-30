import sys
sys.path.append('scmailclient/')
import scmail
import re


PASSWORD = 'scmail'


def create_key(runner, password=PASSWORD):
    result = runner.invoke(scmail.client, ['create', '-p', PASSWORD])
    f = re.findall(r"\[GNUPG\:\] KEY_CREATED P ([A-Z0-9]+)", result.stdout_bytes.decode(), re.S)
    return f[0]


def create_two(runner, password=PASSWORD):
    # create two new keys.
    sender_fingerprint = create_key(runner, password=PASSWORD)
    recipient_fingerprint = create_key(runner, password=PASSWORD)
    return sender_fingerprint, recipient_fingerprint


def register(caplog, runner, fingerprint):
    caplog.set_level(10)
    """register for one key."""
    result = runner.invoke(scmail.client, ['register', '-f', fingerprint])
    assert 'Registration success.' in caplog.text
    caplog.clear()


def send(caplog, runner, sender, recipient, message):
    caplog.set_level(10)
    runner.invoke(scmail.client, ['send', '-s', sender, '-r', recipient, '-m', message])
    assert 'Sending message success.' in caplog.text
    caplog.clear()


def retrieve(caplog, runner, sender, recipient):
    caplog.set_level(10)
    runner.invoke(scmail.client, ['retrieve', '-f', recipient, '-s', sender, '-p', PASSWORD])
