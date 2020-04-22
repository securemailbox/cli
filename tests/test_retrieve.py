import pytest
import sys
sys.path.append('../')
from scmailclient import scmail
from helper import create_two, register


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


@pytest.mark.unfinished
def test_no_sender(caplog, runner):
    pass


@pytest.mark.unfinished
def test_no_message(caplog, runner):
    pass


@pytest.mark.unfinished
def test_one_message(caplog, runner):
    pass


@pytest.mark.unfinished
def test_multiple_messages(caplog, runner):
    pass

