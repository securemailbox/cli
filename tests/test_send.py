import pytest
import sys
sys.path.append('../')
from scmailclient import scmail
from helper import create_two, register


'''
Handle cases of send:

- parameters checking:
    - two fingerprints
    - message.

- success.
- not register
    - both
    - recipient
    - sender
'''


@pytest.mark.finished
def test_no_register(caplog, runner):
    """Two fingerprint not register."""
    sender, recipient = create_two(runner)

    # first, check recipient fingerprint cause the api check it first.
    result = runner.invoke(scmail.client, ['send', '-s', sender, '-r', recipient, '-m', 'from test_recipient_register func. Two fingerprint not register.'])
    assert 'no recipient fingerprint match' in caplog.text


@pytest.mark.finished
def test_recipient_no_register(caplog, runner):
    """Just recipient not register."""
    sender, recipient = create_two(runner)
    # register sender
    register(caplog, runner, sender)

    # check recipient
    runner.invoke(scmail.client, ['send', '-s', sender, '-r', recipient, '-m', f'come from test_recipient_no_register. Only recipient not register.'])
    assert 'Sending message fail.' in caplog.text
    assert 'no recipient fingerprint match' in caplog.text


@pytest.mark.finished
def test_sender_no_register(caplog, runner):
    """Only sender not register."""
    sender, recipient = create_two(runner)
    # second, register for recipient to check sender.
    register(caplog, runner, recipient)

    # check sender.
    runner.invoke(scmail.client, ['send', '-s', sender, '-r', recipient, '-m', f'come from test_sender_no_register. Only sender not register.'])
    assert 'Sending message fail.' in caplog.text
    assert 'no sender fingerprint match' in caplog.text


@pytest.mark.finished
def test_message(caplog, runner):
    """Special character"""
    sender, recipient = create_two(runner)

    # register two
    register(caplog, runner, sender)
    register(caplog, runner, recipient)

    # special character.
    caplog.set_level(10)
    runner.invoke(scmail.client, ['send', '-s', sender, '-r', recipient, '-m', f'come from test_message. Testing special character.\nand\tand\\and\'\"'])
    assert 'Sending message success.' in caplog.text

