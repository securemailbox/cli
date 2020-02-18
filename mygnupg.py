import gnupg

class mygnupg():
    """
    This class used for initial gnupg, 
    create, import, and export key pairs.
    Also, can encrypt and decrypt data.
    """
    def __init__(self):
        """
        The binary file should be different
        in different os.
        This is MacOS version.
        """
        self.gpg = gnupg.GPG(gnupghome='./gnupgkeys')
        self.key = None
        self.email = "john_smith@scmail.org"
        self.keytype = "RSA"
        self.password = "sample"

    def import_key(self, path):
        """
        This function used for check whether the gnupg pub or pvt key already exist.
        If exist, import it, if not, return false.
        """
        try:
            key_data = open(path).read()
            self.key = self.gpg.import_keys(key_data)
        except:
            raise Exception('the file is wrong or not exist!')

    def create(self):
        """
        just create a new key pair. need parameters:
        """
        # parameters
        input_data = self.gpg.gen_key_input(name_email=self.email, key_type=self.keytype, passphrase=self.password)

        # gen key pair
        self.key = self.gpg.gen_key(input_data)

    def export_key(self, tofile=False):
        sc_pub = self.gpg.export_keys(self.key.fingerprint)
        sc_pvt = self.gpg.export_keys(self.key.fingerprint, True, passphrase=self.password)
        # print(sc_pvt)
        if tofile == False:
            return

        # store key for test
        with open('./jskey.asc', 'w') as f:
            f.write(sc_pub)
            f.write(sc_pvt)
        # print('Successful generate a new key.')

    def list(self, sec=False):
        return self.gpg.list_keys(sec)

if __name__ == "__main__":
    mygpg = mygnupg()
    mygpg.import_key('./jskey.asc')
    a = mygpg.list()
    b = mygpg.list(True)
    print(a, '\n', b)
    # gpg.create()
