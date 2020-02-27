import click
from os import getlogin
from gpgopt import GpgOpt

@click.group()
@click.option('--gnupghome', prompt='Enter your gnupg home dir:', default='gnupgkeys', help='The home dir of gnupg key pairs.')
@click.option('--email', prompt='Enter your email:', default=getlogin()+'@scmail.dev', help='The email of user.')
@click.pass_context
def client(ctx, gnupghome, email):
    """
    
    """
    ctx.obj['gpg'] = GpgOpt(mygnupghome=gnupghome, email=email)

@click.command()
@click.password_option('--password', prompt='Enter private key password:', help='Password of private key.')
@click.option('--key-type', prompt='Enter key type:', default="RSA", help='The algorithms to generate the key. ex. RSA')
@click.option('--key-length', prompt='Enter key length:', default=1024, help='The length of the key.')
@click.option('--expire-date', prompt='Enter expire date:', default="2y", help='The expire time of the key pair.')
@click.pass_context
def create_key(ctx, password, key_type, key_length, expire_date):
    print('Those are the information about the key will be created:\n')
    ctx.obj['gpg'].create(password, key_type=key_type, key_length=key_length, expire_date=expire_date)

@click.command()
@click.pass_context
def list_keys(ctx):
    keys = ctx.obj['gpg'].list_keys()
    print(keys)

@click.command()
@click.pass_context
def send(ctx):
    pass

client.add_command(create_key)
client.add_command(list_keys)
client.add_command(send)

if __name__=='__main__':
    client(obj={})

"""
my quick note:
client is the hole client and initial gpg.
have option: gnupg home dir, email.

create key do not need options and the program auto run.

list key have pvt key options.
"""
