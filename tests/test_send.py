import pytest
from helper import scmail, create_two, register, create_key

"""
Handle cases of send:

- parameters checking:
    - two fingerprints
    - message.

- success.
- not register
    - both
    - recipient
    - sender
"""


@pytest.mark.finished
def test_no_register(caplog, runner):
    """Two fingerprint not register."""
    sender, recipient = create_two(caplog, runner)

    # first, check recipient fingerprint cause the api check it first.
    runner.invoke(
        scmail.client,
        [
            "send",
            "-s",
            sender,
            "-r",
            recipient,
            "-m",
            "from test_recipient_register func. Two fingerprint not register.",
        ],
    )
    assert "no recipient fingerprint match" in caplog.text


@pytest.mark.finished
def test_recipient_no_register(caplog, runner):
    """Just recipient not register."""
    sender, recipient = create_two(caplog, runner)
    # register sender
    register(caplog, runner, sender)

    # check recipient
    runner.invoke(
        scmail.client,
        [
            "send",
            "-s",
            sender,
            "-r",
            recipient,
            "-m",
            f"come from test_recipient_no_register. Only recipient not register.",
        ],
    )
    assert "Sending message fail." in caplog.text
    assert "no recipient fingerprint match" in caplog.text


@pytest.mark.finished
def test_sender_no_register(caplog, runner):
    """Only sender not register."""
    sender, recipient = create_two(caplog, runner)
    # second, register for recipient to check sender.
    register(caplog, runner, recipient)

    # check sender.
    runner.invoke(
        scmail.client,
        [
            "send",
            "-s",
            sender,
            "-r",
            recipient,
            "-m",
            f"come from test_sender_no_register. Only sender not register.",
        ],
    )
    assert "Sending message fail." in caplog.text
    assert "no sender fingerprint match" in caplog.text


@pytest.mark.finished
def test_no_encrypt_key(caplog, runner):
    """Create test if no key in gpg."""
    recipient = "0BA99F971B971837D2C87DAED9ECD22814CCD519"
    sender = create_key(caplog, runner)

    # Since the sending will be prevent before request post, do not register.
    # begin run send.
    runner.invoke(
        scmail.client,
        ["send", "-s", sender, "-r", recipient, "-m", "from test_no_encrypt_key."],
    )
    assert "Message encrypt fail." in caplog.text


@pytest.mark.finished
def test_message(caplog, runner):
    """Special character"""
    sender, recipient = create_two(caplog, runner)

    # register two
    register(caplog, runner, sender)
    register(caplog, runner, recipient)

    # special character.
    caplog.set_level(10)
    runner.invoke(
        scmail.client,
        [
            "send",
            "-s",
            sender,
            "-r",
            recipient,
            "-m",
            f"come from test_message. Testing special character.\nand\tand\\and'\"",
        ],
    )
    assert "Sending message success." in caplog.text
