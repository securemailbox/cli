import pytest
import sys
sys.path.append('../')
from scmailclient import scmail
from helper import create_two, register, PASSWORD


'''
Handle cases of retrieve:

- parameter checking
    - two fingerprint

- no message
- one messages
- multiple messages.
-
'''


def send(caplog, runner, sender, recipient, message):
    caplog.set_level(10)
    runner.invoke(scmail.client, ['send', '-s', sender, '-r', recipient, '-m', message])
    assert 'Sending message success.' in caplog.text
    caplog.clear()


@pytest.mark.finished
def test_no_sender(caplog, runner):
    fingerprint, sender = create_two(runner)
    register(caplog, runner, fingerprint)
    register(caplog, runner, sender)

    # send message
    message = 'come from test_no_sender.'
    send(caplog, runner, sender, fingerprint, message)

    # retrieve messages
    caplog.set_level(10)
    runner.invoke(scmail.client, ['retrieve', '-f', fingerprint, '-p', PASSWORD])

    assert ' message successful.' in caplog.text
    assert message in caplog.text


@pytest.mark.finished
def test_no_message(caplog, runner):
    fingerprint, sender = create_two(runner)
    register(caplog, runner, fingerprint)
    register(caplog, runner, sender)

    # retrieve
    caplog.set_level(10)
    runner.invoke(scmail.client, ['retrieve', '-f', fingerprint, '-s', sender, '-p', PASSWORD])

    assert ' message successful.' in caplog.text
    assert 'No message.' in caplog.text


@pytest.mark.finished
def test_one_message(caplog, runner):
    fingerprint, sender = create_two(runner)
    register(caplog, runner, fingerprint)
    register(caplog, runner, sender)

    # send
    message = 'come from test_one_message'
    send(caplog, runner, sender, fingerprint, message)

    # retrieve
    caplog.set_level(10)
    runner.invoke(scmail.client, ['retrieve', '-f', fingerprint, '-s', sender, '-p', PASSWORD])

    assert 'Decrypt 1 message successful.' in caplog.text
    assert message in caplog.text


@pytest.mark.finished
def test_multiple_messages(caplog, runner):
    fingerprint, sender = create_two(runner)
    register(caplog, runner, fingerprint)
    register(caplog, runner, sender)

    # send
    messages = ['first message', 'second message', 'third message', 'multiple message']
    for message in messages:
        send(caplog, runner, sender, fingerprint, message)

    # retrieve
    caplog.set_level(10)
    runner.invoke(scmail.client, ['retrieve', '-f', fingerprint, '-s', sender, '-p', PASSWORD])

    assert f'Decrypt {len(messages)} message successful.' in caplog.text
    for message in messages:
        assert message in caplog.text

