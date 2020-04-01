import requests
import click
import pprint
import re
from pathlib import Path
from os import environ
import getpass
from gpgopt import GpgOpt
import logging
import time

# Default to localhost if url is not given
SECUREMAILBOX_URL = environ.get("SECUREMAILBOX_URL", "http://127.0.0.1:8080")

# Logging Level
LOGGING_LEVEL = environ.get("LOGGING_LEVEL", logging.DEBUG)

@click.group()
@click.pass_context
def client(ctx):
    """Initial client."""
    # Bacis config of logging
    Path('log').mkdir(exist_ok=True)
    times = time.strftime("%Y%m%d%H%M%S",time.localtime())
    logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s',
        level=LOGGING_LEVEL,
        handlers=[
            logging.FileHandler(filename=Path('log', times)),
            logging.StreamHandler()
        ]
    )
    ctx.logger = logging.getLogger(__name__)

    # Set config file path.
    ctx.config = Path('scmail.conf')

    # If the config not exist, set user information. If not, run initial gpg.
    gnupghome, email = load_config() if ctx.config.exists() else ctx.invoke(set_user_info, gnupghome=click.prompt('Enter your gnupg home dir:', default='gnupgkeys'), email=click.prompt('Enter your email:', default= f'{getpass.getuser()}@scmail.dev'))
    # ctx.obj.get('logger').debug(f'gnupg home is {gnupghome}, email is {email}')
    ctx.logger.debug(f'gnupg home is {gnupghome}, email is {email}')

    # ctx.obj['gpg'] = GpgOpt(mygnupghome=gnupghome, email=email)
    ctx.gpg = GpgOpt(mygnupghome=gnupghome, email=email)

    # Initial pretty printer
    ctx.pp = pprint.PrettyPrinter(indent=2)

    logging.info('Initialize client successful.')


@click.pass_context
def load_config(ctx):
    """Load config file."""
    f = ctx.config.open('r').read()
    config = re.split('\n|=', f)

    for i in range(0, len(config), 2):
        print(f'The {config[i]} is: {config[i+1]}')

    print()
    logging.info('Config file exists. Load Successful.')
    return config[1], config[3]


@click.pass_context
def set_user_info(ctx, gnupghome, email):
    """Set user information and return gnupghome and email."""
    config = 'gnupghome=' + gnupghome + '\n' + 'email=' + email

    # Store config file and other information.
    ctx.config.touch(exist_ok=False)
    with ctx.config.open('w') as f:
        f.write(config)

    logging.info('Setting user information finish.')
    return gnupghome, email


# @click.command()
# @click.option('--gnupghome', prompt='Enter your gnupg home dir', default='gnupgkeys',
#               help='The home dir of gnupg key pairs.')
# @click.option('--email', prompt='Enter your email', default=getlogin() + '@scmail.dev', help='The email of user.')
# @click.pass_context
# def update_user_info(ctx, gnupghome, email):
#     """Update gnupg home dir and personal email"""
#     pass


@click.command()
@click.option('--key-type', prompt='Enter key type', default="RSA", help='The algorithms to generate the key. ex. RSA')
@click.option('--key-length', prompt='Enter key length', default=1024, help='The length of the key.')
@click.option('--expire-date', prompt='Enter expire date', default="2y", help='The expire time of the key pair. 0 or empty for never expire.')
@click.password_option('--password', prompt='Enter private key password', help='Password of private key.')
@click.pass_context
def create_key(ctx, key_type, key_length, expire_date, password):
    """Create gnupg key pairs."""
    logging.debug(f'Information about key:\nkey type: {key_type}\nkey length: {key_length}\nexpire date: {expire_date}\n')

    # Warning if key never expire and user want to continue.
    if expire_date == 0 and not click.confirm('0 means never expire, Do you want to continue?'):
        logging.warning('Never expire key will be created.')

    key = ctx.parent.gpg.create(password, key_type=key_type, key_length=key_length, expire_date=expire_date)
    ctx.parent.pp.pprint(key.__dict__)
    logging.info('Key Creation finished.')


@click.command()
@click.option('--show-private', prompt='Do you want to show the private keys?', default=False, is_flag=True,
              help='Whether show the private keys')
@click.pass_context
def list_keys(ctx, show_private):
    """List and print all the keys in the gnupg home dir."""
    keys = ctx.parent.gpg.list_keys(show_private)
    key_type = 'public' if show_private is False else 'private'

    logging.info(f'{len(keys)} {key_type} keys exist.')
    ctx.parent.pp.pprint(keys.__dict__)
    logging.info('List keys finished.')


@click.command()
@click.pass_context
def register(ctx):
    """Register sc_mail API."""
    # Request register.
    logging.debug('begin register.')
    fingerprint = ctx.parent.gpg.list_keys(True).curkey.get('fingerprint')
    logging.debug(f'Getting fingerprint: {fingerprint}')
    data = {'fingerprint': fingerprint}

    # Register
    r = requests.post(SECUREMAILBOX_URL + '/register/', json=data)
    logging.debug(f'response is: \n{r}')
    res = r.json()
    logging.debug(f'response is: \n{res}')

    if r.status_code == 200:
        logging.info('Registration success.')
        ctx.parent.pp.pprint(r.json())
    else:
        logging.error(f'Registration fail.\nError {r.status_code} is: {res.get("error")}')


@click.command()
@click.option('--recipient', prompt='The recipient', required=True, help='The email address of the recipient.')
@click.password_option('--password', prompt='Enter passwordo of private key to decrypt', help='The passphrase of private key')
@click.pass_context
def retrieve(ctx, recipient, password):
    """Retrieve and Post messages from API"""
    data = {'fingerprint': ctx.parent.gpg.list_keys(False).curkey.get('fingerprint')}
    # Retrieve
    r = requests.post(SECUREMAILBOX_URL + '/retrieve/', json=data)
    res = r.json()

    if r.status_code == 200:
        logging.info('The message retrieve successful.')
    else:
        logging.error(f'The message retrieve fail.\nError {r.status_code} is: {res.get("error")}')
        return

    # Decrypt the messages.
    ok, messages = ctx.parent.gpg.decrypt_message(messages=res.get('error'), passphrase=password)
    ctx.parent.pp.pprint(messages[:-1])
    if ok is False:
        logging.error(f'Other message decrypt fail.\n{messages[-1]}')
    else:
        ctx.parent.pp.pprint(messages[-1])
        logging.info('Decrypt message successful.')


@click.command()
@click.option('--recipient', prompt='The recipient fingerprint', required=True, help='The fingerprint of the recipient.')
@click.option('--message', required=True, prompt='The message', help='Message that will send.')
@click.pass_context
def send(ctx, recipient, message):
    """Send a message.

    recipient: the fingerprint of recipient

    message: the messages.
    """
    # Choose recipient and Encrypted
    ok, encrypted_message = ctx.parent.gpg.encrypt_message(message, recipient)
    if ok is False:
        logging.error(f'Message encrypt fail.\n{encrypted_message}')
    else:
        logging.info('Message encrypt success.')

    # Send
    payload = {'fingerprint': recipient, 'message': message}
    r = requests.post(SECUREMAILBOX_URL + '/send/', json=payload)

    if r.status_code == 200:
        logging.info('Sending message success.')
    else:
        logging.error(f'Sending message fail.\nError {r.status_code} is: {r.json().get("error")}')


@click.command()
@click.option('--fingerprint', prompt='Enter the fingerprint of that key', required=True, help='The fingerprint of exported key.')
@click.option('--is-file', prompt='Do you want to store keys to file (or print)?', is_flag=True, help='Whether export to file.')
@click.option('--is-pvt', prompt='Do you want to export private key?', is_flag=True, help='Whether export private keys.')
@click.pass_context
def export_key(ctx, fingerprint, is_file, is_pvt):
    file_name = None
    passphrase = None

    if is_file is True:
        file_name = click.prompt('Enter the file name', type=str)
        try:
            file_name = Path(file_name)
            file_name.touch(exist_ok=False)
            logging.debug('file not exists.')
        except FileExistsError:
            logging.error('Cause the path already exist, export to file failed.')
            logging.warning('Mail Client Exit.')
            if click.confirm('Do you want to print on console?', default=True):
                is_file = False
            else:
                return

            pass

    if is_pvt is True:
        passphrase = click.prompt('Enter pvt\'s passphrase', hide_input=True, type=str)

    pub, pvt = ctx.parent.gpg.export_key(fingerprint, export_pvt=is_pvt, password=passphrase)

    if is_file is False:
        ctx.parent.pp.pprint(pub)
        if is_pvt is True:
            ctx.parent.pp.pprint(pvt)
    else:
        with file_name.open('w') as f:
            f.write(pub)
            f.write(pvt)

    logging.info('Export key successful.')


@click.command()
@click.pass_context
def import_key(ctx, path):
    pass


# client.add_command(update_user_info)
client.add_command(create_key)
client.add_command(list_keys)
client.add_command(register)
client.add_command(send)
client.add_command(retrieve)
client.add_command(export_key)
client.add_command(import_key)


if __name__ == '__main__':
    client()
