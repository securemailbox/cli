import pytest
from helper import create_two, register, PASSWORD, send, scmail, create_key


"""
Handle cases of retrieve:

- parameter checking
    - two fingerprint

- no message
- one messages
- multiple messages.
-
"""


@pytest.mark.finished
def test_no_sender(caplog, runner):
    fingerprint, sender = create_two(runner)
    register(caplog, runner, fingerprint)
    register(caplog, runner, sender)

    # send message
    message = "come from test_no_sender."
    send(caplog, runner, sender, fingerprint, message)

    # retrieve messages
    caplog.set_level(10)
    runner.invoke(scmail.client, ["retrieve", "-f", fingerprint, "-p", PASSWORD])

    assert " message successful." in caplog.text
    assert message in caplog.text


@pytest.mark.finished
def test_no_message(caplog, runner):
    fingerprint, sender = create_two(runner)
    register(caplog, runner, fingerprint)
    register(caplog, runner, sender)

    # retrieve
    caplog.set_level(10)
    runner.invoke(
        scmail.client, ["retrieve", "-f", fingerprint, "-s", sender, "-p", PASSWORD]
    )

    assert "Retrieve message successful. No message available." in caplog.text


@pytest.mark.finished
def test_one_message(caplog, runner):
    fingerprint, sender = create_two(runner)
    register(caplog, runner, fingerprint)
    register(caplog, runner, sender)

    # send
    message = "come from test_one_message"
    send(caplog, runner, sender, fingerprint, message)

    # retrieve
    caplog.set_level(10)
    runner.invoke(
        scmail.client, ["retrieve", "-f", fingerprint, "-s", sender, "-p", PASSWORD]
    )

    assert "Decrypt 1 message successful." in caplog.text
    assert message in caplog.text


@pytest.mark.finished
def test_one_message_wrong_sender(caplog, runner):
    fingerprint, sender = create_two(runner)
    wrong_sender = create_key(runner)

    # register three
    register(caplog, runner, fingerprint)
    register(caplog, runner, sender)
    register(caplog, runner, wrong_sender)

    message = "come from test_one_message_wrong_sender"
    send(caplog, runner, sender, fingerprint, message)

    # retrieve
    caplog.set_level(10)
    runner.invoke(
        scmail.client,
        ["retrieve", "-f", fingerprint, "-s", wrong_sender, "-p", PASSWORD],
    )

    # check no message retrieve
    assert "Retrieve message successful. No message available." in caplog.text


@pytest.mark.finished
def test_multiple_messages(caplog, runner):
    fingerprint, sender = create_two(runner)
    register(caplog, runner, fingerprint)
    register(caplog, runner, sender)

    # send
    messages = ["first message", "second message", "third message", "multiple message"]
    for message in messages:
        send(caplog, runner, sender, fingerprint, message)

    # retrieve
    caplog.set_level(10)
    runner.invoke(
        scmail.client, ["retrieve", "-f", fingerprint, "-s", sender, "-p", PASSWORD]
    )

    assert f"Decrypt {len(messages)} message successful." in caplog.text
    for message in messages:
        assert message in caplog.text
