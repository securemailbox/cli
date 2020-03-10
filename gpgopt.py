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
        print(mygnupghome)
        p = Path(mygnupghome)
        if p.exists() is False:
            p.mkdir(parents=True)
        self.gpg = gnupg.GPG(gnupghome=mygnupghome)
        self.key = None
        self.email = email

    def import_key(self, path):
        """Check whether the gnupg pub or pvt key already exist.
        If exist, import it, if not, return false.
        """
        key_data = open(path).read()
        self.key = self.gpg.import_keys(key_data)

    def create(self, password, key_type="RSA", key_length=1024, expire_date="2y"):
        """Create a new key pair. need parameters:

        Keyword arguments:
        password -- required. the password of your pvt key.
        key_type -- optional, algorithms to generate the key.
        key_length -- optional, 
        """
        # all parameters that user can choose.
        input_data = self.gpg.gen_key_input(name_email=self.email, key_type=key_type, passphrase=password,
                                            key_length=key_length, expire_date=expire_date)

        # generate key pair
        # {'fingerprint': '', }
        return self.gpg.gen_key(input_data)

    def export_key(self, export_pvt=False, password=None, to_file=False, path=None):
        """
        """
        sc_pub = self.gpg.export_keys(self.key.fingerprint)
        sc_pvt = self.gpg.export_keys(self.key.fingerprint, False, passphrase=password)

        # print pub and pvt to the command line.
        print(sc_pub, sc_pvt)

        if to_file is False:
            return
        try:
            # store key to file
            with open(path, 'w') as f:
                f.write(sc_pub)
                f.write(sc_pvt)
        finally:
            raise Exception("the path not exist")

    def list_keys(self, sec=False):
        """Get pub or pvt keys and return them."""
        return self.gpg.list_keys(secret=sec)


if __name__ == "__main__":
    mygpg = GpgOpt()
    mygpg.create('abcddeeff')
    b = mygpg.list_keys(sec=False)
    print(b)
    # mygpg.export_key(False, 'abcddeeff', False, './jskey.asc')
    # mygpg.import_key('./jskey.asc')
