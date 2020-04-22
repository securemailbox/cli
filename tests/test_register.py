import pytest
import sys
sys.path.append('../')
from scmailclient import scmail
from helper import create_key


'''
Three test cases.
- fingerprint exists
- fingerprint length error
    - long
    - short
    - normal

Because fingerprint is only one parameter, length normal cause equal to success cause.

Cause click prompt not allow no fingerprint case happened, there is no test case about it.
'''


NORMAL_FINGERPRINT = 'FAC10F0C3D1D49F8F9A82CB553E79F7C92E1CF33'


@pytest.mark.finished
@pytest.mark.parametrize('fingerprint',
                         ['shortafingerprint',
                          'longafingerprintfdjlaeiemalmcklaeiojr243232l3kjl34j2'])
def test_fingerprint_length(caplog, runner, fingerprint):
    runner.invoke(scmail.client, ['register', '-f', fingerprint])

    if fingerprint != 40:
        assert 'not a valid length' in caplog.text
    else:
        assert 'Registration success' in caplog.text


@pytest.mark.finished
def test_fingerprint_exists(caplog, runner):
    fingerprint = create_key(runner)
    runner.invoke(scmail.client, ['register', '-f', fingerprint])
    caplog.clear()

    runner.invoke(scmail.client, ['register', '-f', fingerprint])

    assert 'already exists' in caplog.text

