import pytest
from helper import scmail, create_key


"""
Three test cases.
- fingerprint exists
- fingerprint length error
    - long
    - short
    - normal

Because fingerprint is only one parameter, length normal cause equal to success cause.

Cause click prompt not allow no fingerprint case happened, there is no test case about it.
"""


@pytest.mark.finished
@pytest.mark.parametrize(
    "fingerprint",
    ["shortafingerprint", "longafingerprintfdjlaeiemalmcklaeiojr243232l3kjl34j2"],
)
def test_fingerprint_length(caplog, runner, fingerprint):
    runner.invoke(scmail.client, ["register", "-f", fingerprint])

    assert "not a valid length" in caplog.text


@pytest.mark.finished
def test_fingerprint_exists(caplog, runner):
    fingerprint = create_key(runner)
    # register first time
    runner.invoke(scmail.client, ["register", "-f", fingerprint])
    # assert 'Registration success.' in caplog.text
    caplog.clear()

    # register second times.
    caplog.set_level(10)
    runner.invoke(scmail.client, ["register", "-f", fingerprint])
    assert "already exists" in caplog.text
