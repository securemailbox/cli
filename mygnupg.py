import gnupg
from pathlib import Path
from os import getlogin
from random import randint

class GpgOpt():
    """
    This class used for initial gnupg, 
    create, import, and export key pairs.
    Also, can encrypt and decrypt data.
    """
    def __init__(self, password, mygnupghome='gnupgkeys', email=os.getlogin()+'@', key_type="RSA"):
        """
        """
        p = Path(mygnupghome)
        self.gpg = gnupg.GPG(gnupghome=mygnupghome.name)
        self.key = None
        self.email = email
        self.key_type = key_type
        self.password = password

    def import_key(self, path):
        """
        This function used for check whether the gnupg pub or pvt key already exist.
        If exist, import it, if not, return false.
        """
        key_data = open(path).read()
        self.key = self.gpg.import_keys(key_data)

    def create(self):
        """
        just create a new key pair. need parameters:
        """
        # parameters
        input_data = self.gpg.gen_key_input(name_email=self.email, key_type=self.keytype, passphrase=self.password)

        # gen key pair
        self.key = self.gpg.gen_key(input_data)

    def export_key(self, to_file=False, path=None):
        sc_pub = self.gpg.export_keys(self.key.fingerprint)
        sc_pvt = self.gpg.export_keys(self.key.fingerprint, True, passphrase=self.password)
        print(sc_pub, sc_pvt)

        if to_file == False:
            return

        # store key for test
        with open(path, 'w') as f:
            f.write(sc_pub)
            f.write(sc_pvt)
        # print('Successful generate a new key.')

    def list(self, sec=False):
        return self.gpg.list_keys(sec)

if __name__ == "__main__":
    mygpg = GpgOpt()
    mygpg.create()
    # mygpg.export_key()
    mygpg.export_key(True, './jskey.asc')
    mygpg.import_key('./jskey.asc')
    a = mygpg.list()