import gnupg
from pathlib import Path
from random import randint
import logging

# For Testing
import time
import getpass


class GpgOpt():
    """Initial gnupg, create, import, and export key pairs.

    create, import, and export key pairs.
    Also, can encrypt and decrypt message.
    """

    def __init__(self, mygnupghome):
        """
        """
        Path(mygnupghome).mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self.logger.debug('Home Dir of GnuPG exists.')

        self.gpg = gnupg.GPG(gnupghome=mygnupghome)
        self.logger.info('Initialize GnuPG successful.')


    def import_key(self, key_data):
        """Check whether the gnupg pub or pvt key already exist.

        If exist, import it, if not, return false.
        """
        result = self.gpg.import_keys(key_data=key_data)
        return {'success': result.results, 'imported': result.imported, 'counts': result.counts}


    def create(self, password, name, email, key_type, key_length, expire_date):
        """Create a new key pair. need parameters:

        Keyword arguments:

        password: required. the password of your pvt key.

        name: optional, the name of user.

        email: optional, the email address of user.

        key_type: optional, algorithms to generate the key.

        key_length: optional, the length of key.

        expire_date: optional, expire date of this key.
        """
        # all parameters that user can choose.
        input_data = self.gpg.gen_key_input(
            name_real=name,
            name_email=email,
            key_type=key_type,
            passphrase=password,
            key_length=key_length,
            expire_date=expire_date)

        # generate key pair
        return self.gpg.gen_key(input_data)


    def export_key(self, fingerprint, export_pvt=False, password=None):
        """Export key pair from the gnupg."""
        sc_pub = self.gpg.export_keys(fingerprint)
        sc_pvt = None

        if export_pvt is True and password is not None:
            sc_pvt = self.gpg.export_keys(fingerprint, True, passphrase=password)

        return sc_pub, sc_pvt


    def list_keys(self, sec=False):
        """Get pub or pvt keys and return them."""
        return self.gpg.list_keys(secret=sec)


    def scan_file(self, file_path):
        """Scan the keys in a file."""
        return self.gpg.scan_keys(file_path)


    def encrypt_message(self, message, recipient):
        """Encrypt the message and return the encrypted message.

        message: string message.

        email: string, email of recipient.
        """
        msg = self.gpg.encrypt(message, recipient, always_trust=True)
        return (True, msg.data) if msg.ok else (False, msg.stderr)


    def decrypt_message(self, messages, passphrase):
        """Decrypt the message and return the original message.

        message: list of string messages.

        passphrase: string, passphrase of the private key.
        """
        msgs = []
        tag = True

        if messages is None:
            msgs = ['No message.']
            return (True, msgs)

        for message in messages:
            msg = self.gpg.decrypt(message=message, passphrase=passphrase)
            if msg.ok is False:
                msgs.append(msg.stderr)
                tag = False
            msgs.append(msg.data)

        return (tag, msgs)


if __name__ == "__main__":
    mygpg = GpgOpt(mygnupghome='gnupgkeys')
    LOG_TIME_FORMAT = time.strftime("%Y%m%d%H%M%S",time.localtime())
    LOGGING_LEVEL = logging.DEBUG
    logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s',
        level=LOGGING_LEVEL,
        handlers=[
            logging.FileHandler(filename=Path('log', LOG_TIME_FORMAT)),
            logging.StreamHandler()
        ]
    )
    # Test import key
    path = 'b'
    res = mygpg.import_key(path=path)
    print(res)
