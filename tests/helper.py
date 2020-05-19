import sys

sys.path.append("scmailclient/")
import scmail
import re

PASSWORD = "scmail_testing"


def create_key(caplog, runner, password=PASSWORD):
    caplog.set_level(10)
    runner.invoke(scmail.client, ["create-key", "-p", password])
    f = re.findall(r"Fingerprint is ([0-9A-Z]+).", caplog.text, re.S)
    caplog.clear()
    return f[0]


def create_two(caplog, runner):
    # create two new keys.
    sender_fingerprint = create_key(caplog, runner)
    recipient_fingerprint = create_key(caplog, runner)
    return sender_fingerprint, recipient_fingerprint


def register(caplog, runner, fingerprint):
    caplog.set_level(10)
    """register for one key."""
    result = runner.invoke(scmail.client, ["register", "-f", fingerprint])
    assert "Registration success." in caplog.text
    caplog.clear()


def send(caplog, runner, sender, recipient, message):
    caplog.set_level(10)
    runner.invoke(scmail.client, ["send", "-s", sender, "-r", recipient, "-m", message])
    assert "Sending message success." in caplog.text
    caplog.clear()


def retrieve(caplog, runner, sender, recipient, password=PASSWORD):
    caplog.set_level(10)
    runner.invoke(
        scmail.client, ["retrieve", "-f", recipient, "-s", sender, "-p", password]
    )
