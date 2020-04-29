from helper import scmail, register, create_key, send, PASSWORD, retrieve
import pytest


'''
This is an aggregation test about multiple people using API.
'''


@pytest.mark.finished
def test_two_people(caplog, runner):
    # create and register.
    alice_p = 'alice'
    bob_p = 'bob'
    alice_finger = create_key(runner, password=alice_p)
    bob_finger = create_key(runner, password=bob_p)
    register(caplog, runner, alice_finger)
    register(caplog, runner, bob_finger)

    alice_message = 'Hi Bob, my name is Alice. Nice to meet you.'
    send(caplog, runner, sender=alice_finger, recipient=bob_finger, message=alice_message)
    caplog.set_level(10)
    runner.invoke(scmail.client, ['retrieve', '-f', bob_finger, '-s', alice_finger, '-p', bob_p])
    assert alice_message in caplog.text
    caplog.clear()

    bob_message = 'Hello Bob, nice to meet you too.'
    send(caplog, runner, sender=bob_finger, recipient=alice_finger, message=bob_message)
    caplog.set_level(10)
    runner.invoke(scmail.client, ['retrieve', '-f', alice_finger, '-s', bob_finger, '-p', alice_p])
    assert bob_message in caplog.text
    caplog.clear()


@pytest.mark.unfinished
def test_five_people(caplog, runner):
    pass

