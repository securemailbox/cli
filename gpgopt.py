import gnupg
from pathlib import Path
from os import getlogin
from random import randint


class GpgOpt():
    """Initial gnupg, create, import, and export key pairs.

    create, import, and export key pairs.
    Also, can encrypt and decrypt message.
    """

    def __init__(self, mygnupghome='gnupgkeys', email=getlogin() + '@scmail.dev'):
        """
        """
        p = Path(mygnupghome)
        if p.exists() is False:
            p.mkdir(parents=True)

        self.gpg = gnupg.GPG(gnupghome=mygnupghome)
        self.email = email


    def import_key(self, path):
        """Check whether the gnupg pub or pvt key already exist.
        If exist, import it, if not, return false.
        """
        key_data = open(path).read()


    def create(self, password, key_type="RSA", key_length=1024, expire_date="2y"):
        """Create a new key pair. need parameters:

        Keyword arguments:
        password: required. the password of your pvt key.
        key_type: optional, algorithms to generate the key.
        key_length: optional, 
        """
        # all parameters that user can choose.
        input_data = self.gpg.gen_key_input(name_email=self.email, key_type=key_type, passphrase=password,
                                            key_length=key_length, expire_date=expire_date)

        # generate key pair
        return self.gpg.gen_key(input_data)


    def export_key(self, fingerprint, export_pvt=False, password=None, to_file=False, path=None):
        """Export key pair from the gnupg."""
        sc_pub = self.gpg.export_keys(fingerprint)
        sc_pvt = None

        if export_pvt is True and password is not None:
            sc_pvt = self.gpg.export_keys(fingerprint, True, passphrase=password)

        if to_file is False:
            pass
        try:
            # store key to file
            with open(path, 'w') as f:
                f.write(sc_pub)
                f.write(sc_pvt)
        finally:
            raise Exception("the path not exist")

        return sc_pub, sc_pvt


    def list_keys(self, sec=False):
        """Get pub or pvt keys and return them."""
        return self.gpg.list_keys(secret=sec)


    def encrypt_message(self, message, email):
        """Encrypt the message and return the encrypted message.

        message: string message.
        email: string, email of recipient.
        """
        msg = self.gpg.encrypt(message, email)
        return (True, msg.data) if msg.ok else (False, msg.stderr)


    def decrypt_message(self, messages, passphrase):
        """Decrypt the message and return the original message.

        message: list of string messages.
        passphrase: string, passphrase of the private key.
        """
        msgs = []
        for message in messages:
            msg = self.gpg.decrypt(message=message, passphrase=passphrase)
            if msg.ok is False:
                msgs.append(msg.stderr)
                return (False, msgs)
            msgs.append(msg.data)
        return (True, msgs)


if __name__ == "__main__":
    mygpg = GpgOpt()
    mygpg.create('1')
    # t = mygpg.list_keys(True)
    # f = mygpg.list_keys(False)
    # mygpg.export_key(t.curkey['fingerprint'], True, '1')
    # print(t.__dict__)
    # print(f.__dict__)
