import sys
sys.path.append('../')
from scmailclient import scmail
import re


PASSWORD = 'scmail'


def create_key(runner):
    result = runner.invoke(scmail.client, ['create', '-p', PASSWORD])
    f = re.findall(r"\[GNUPG\:\] KEY_CREATED P ([A-Z0-9]+)", result.stdout_bytes.decode(), re.S)
    return f[0]


def create_two(runner):
    # create two new keys.
    sender_fingerprint = create_key(runner)
    recipient_fingerprint = create_key(runner)
    return sender_fingerprint, recipient_fingerprint


def register(runner, fingerprint):
    """register for one key."""
    result = runner.invoke(scmail.client, ['register', '-f', fingerprint])

