import click
import pprint
import re
from pathlib import Path
from os import environ
import logging
import requests

from gpgopt import GpgOpt
from constants import TIMES, USER_NAME

# Default to localhost if url is not given
SECUREMAILBOX_URL = environ.get("SECUREMAILBOX_URL", "http://localhost:8082/")

# Logging Level
LOGGING_LEVEL = environ.get("LOGGING_LEVEL", logging.INFO)


def check_fingerprint(ctx, param, fingerprint=""):
    # in normal case or it is optional.
    if len(fingerprint) == 40 or not fingerprint:
        return fingerprint
    logging.error("The length of fingerprint is not a valid length.")
    ctx.exit(1)


@click.group(chain=True)
@click.pass_context
def client(ctx):
    """Initial client."""
    # Bacis config of logging
    Path("log").mkdir(exist_ok=True)
    logging.basicConfig(
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        level=LOGGING_LEVEL,
        handlers=[
            logging.FileHandler(filename=Path("log", TIMES)),
            logging.StreamHandler(),
        ],
    )

    # Set config file path.
    ctx.config = Path("scmail.conf")

    # If the config not exist, set user information. If not, run initial gpg.
    gnupghome = (
        load_config()
        if ctx.config.exists()
        else ctx.invoke(
            set_user_info,
            gnupghome=click.prompt("Enter your gnupg home dir:", default="gnupgkeys"),
        )
    )
    ctx.gpg = GpgOpt(mygnupghome=gnupghome)

    # Initial pretty printer
    ctx.pp = pprint.PrettyPrinter(indent=2)

    logging.info("Initialize client successful.")


@click.pass_context
def load_config(ctx):
    """Load config file."""
    with ctx.config.open("r") as f:
        f = f.read()

    config = re.split("\n|=", f)
    logging.debug(f"read config file:{config}")

    for i in range(0, len(config) - 1, 2):
        logging.info(f"The {config[i]} is: {config[i + 1]}")

    logging.info("Config file exists. Load Successful.")
    return config[1]


@click.pass_context
def set_user_info(ctx, gnupghome):
    """Set user information and return gnupghome and email."""
    config = "gnupghome=" + gnupghome + "\n"

    # Store config file and other information.
    ctx.config.touch(exist_ok=False)
    with ctx.config.open("w") as f:
        f.write(config)

    logging.info("Setting user information finish.")
    return gnupghome


@click.command(name="create-key")
@click.option(
    "--name",
    "-n",
    prompt="Enter Name",
    default=USER_NAME,
    type=str,
    help="Generator name.",
)
@click.option(
    "--email",
    "-e",
    prompt="Enter Email",
    default=f"{USER_NAME}@scmail.dev",
    type=str,
    help="The user email address.",
)
@click.option(
    "--key-type",
    "-t",
    prompt="Enter key type",
    default="RSA",
    type=str,
    help="The algorithms to generate the key. ex. RSA",
)
@click.option(
    "--key-length",
    "-l",
    prompt="Enter key length",
    default=1024,
    type=int,
    help="The length of the key.",
)
@click.option(
    "--expire-date",
    "-d",
    prompt="Enter expire date",
    default="2y",
    type=str,
    help="The expire time of the key pair. 0 or empty for never expire.",
)
@click.pass_context
def create_key(ctx, name, email, key_type, key_length, expire_date):
    """Create gnupg key pairs."""
    logging.debug(
        f"Information about key:\nName: {name}\nEmail: {email}\nkey type: {key_type}\nkey length: {key_length}\nexpire date: {expire_date}\n"
    )

    # Warning if key never expire and user want to continue.
    if expire_date == "0":
        if click.confirm("0 means never expire, Do you want to continue?"):
            logging.warning("Never expire key will be created.")
        else:
            logging.info("Not create never expire key.")
            return

    key = ctx.parent.gpg.create(
        name=name,
        email=email,
        key_type=key_type,
        key_length=key_length,
        expire_date=expire_date,
    )
    logging.info(f"Key Creation finished.\nFingerprint is {key.fingerprint}.")


@click.command(name="list-keys")
@click.option(
    "--private",
    "-p",
    prompt="Do you want to show the private keys?",
    default=False,
    type=bool,
    is_flag=True,
    help="Whether show the private keys",
)
@click.pass_context
def list_keys(ctx, private):
    """List and print all the keys in the gnupg home dir."""
    keys = ctx.parent.gpg.list_keys(private)

    length = len(keys)
    logging.info(f"{length} {'public' if private is False else 'private'} keys exist.")
    if not length:
        ctx.exit(1)

    click.secho("Current key is:")
    click.secho(keys.curkey.get("fingerprint"))
    click.secho("All keys are:")
    for key, value in keys.key_map.items():
        click.secho(value.get("fingerprint"))

    logging.info("List keys finished.")


@click.command()
@click.option(
    "--fingerprint",
    "-f",
    prompt="Register fingerprint",
    callback=check_fingerprint,
    required=True,
    type=str,
    help="The fingerprint used to register.",
)
@click.pass_context
def register(ctx, fingerprint):
    """Register scmail API."""
    # Request register.
    logging.info("begin register.")
    logging.debug(f"Getting fingerprint: {fingerprint}")
    data = {"fingerprint": fingerprint}

    # Register
    r = requests.post(SECUREMAILBOX_URL + "/register/", json=data)
    res = r.json()
    logging.debug(f"response is: \n{res}")

    if r.status_code == 201 and res.get("success"):
        logging.info("Registration success.")
        click.secho(fingerprint)
    else:
        logging.error(
            f'Registration fail.\nError {r.status_code} is: {res.get("error")}'
        )


@click.command()
@click.option(
    "--fingerprint",
    "-f",
    prompt="Enter fingerprint of mailbox",
    callback=check_fingerprint,
    required=True,
    type=str,
    help="The fingerprint of the yourself mailbox.",
)
@click.option(
    "--sender-fingerprint",
    "-s",
    prompt="Enter the fingerprint of sender",
    callback=check_fingerprint,
    required=False,
    default="",
    type=str,
    help="The senders fingerprint.",
)
@click.password_option(
    "--password",
    "-p",
    type=str,
    default="None",
    prompt="Enter password of private key",
    help="The passphrase of private key",
)
@click.pass_context
def retrieve(ctx, fingerprint, sender_fingerprint, password):
    """Retrieve and Post messages from API"""
    # Prepare send data.
    logging.debug(fingerprint, sender_fingerprint)
    payload = {"fingerprint": fingerprint}
    if sender_fingerprint:
        payload.update({"sender_fingerprint": sender_fingerprint})

    # Retrieve from api.
    r = requests.post(SECUREMAILBOX_URL + "/retrieve/", json=payload)
    res = r.json()

    if r.status_code == 200:
        logging.info("The message retrieve successful.")
    else:
        logging.error(
            f'The message retrieve fail.\nError {r.status_code} is: {res.get("error")}'
        )
        return

    # load messages.
    logging.debug(f"response is: {res}")

    # if no message retrieve, directly return.
    if res.get("data").get("count") == 0:
        logging.info("Retrieve message successful. No message available.")
        return

    # all messages should be a list of message come from api.
    all_messages = res.get("data").get("messages")
    all_messages = [message.get("message") for message in all_messages]
    logging.debug(all_messages)

    # Decrypt the messages.
    ok, messages = ctx.parent.gpg.decrypt_message(
        messages=all_messages, passphrase=password,
    )
    logging.debug(messages)

    # Decode and Print all message.
    for m in messages:
        click.secho(m.decode("utf-8"))

    if ok is False:
        logging.error(f"Some messages decrypt fail.")
    else:
        logging.info(f"Decrypt {len(messages)} message successful.")


@click.command()
@click.option(
    "--sender-fingerprint",
    "-s",
    prompt="The sender fingerprint",
    callback=check_fingerprint,
    required=True,
    type=str,
    help="The fingerprint of the sender.",
)
@click.option(
    "--recipient",
    "-r",
    prompt="The recipient fingerprint",
    callback=check_fingerprint,
    required=True,
    type=str,
    help="The fingerprint of the recipient.",
)
@click.option(
    "--message",
    "-m",
    required=True,
    prompt="The message",
    type=str,
    help="Message that will send.",
)
@click.pass_context
def send(ctx, sender_fingerprint, recipient, message):
    """Send a message.

    recipient: the fingerprint of recipient

    message: the messages.
    """
    # Choose recipient and Encrypted
    ok, encrypted_message = ctx.parent.gpg.encrypt_message(message, recipient)
    if ok is False:
        logging.error(f"Message encrypt fail.\n{encrypted_message}")
        return
    else:
        logging.info("Message encrypt success.")

    # Send
    payload = {
        "fingerprint": recipient,
        "message": encrypted_message.decode(),
        "sender_fingerprint": sender_fingerprint,
    }
    r = requests.post(SECUREMAILBOX_URL + "/send/", json=payload)
    res = r.json()

    if r.status_code == 201 and res.get("success"):
        logging.info("Sending message success.")
    else:
        logging.error(
            f'Sending message fail.\nError {r.status_code} is: {res.get("error")}'
        )


@click.command(name="export-key")
@click.option(
    "--fingerprint",
    prompt="Enter the fingerprint of that key",
    callback=check_fingerprint,
    required=True,
    type=str,
    help="The fingerprint of exported key.",
)
@click.option(
    "--is-file",
    prompt="Do you want to store keys to file (or print)?",
    type=bool,
    is_flag=True,
    help="Whether export to file.",
)
@click.option(
    "--is-pvt",
    prompt="Do you want to export private key?",
    type=bool,
    is_flag=True,
    help="Whether export private keys.",
)
@click.pass_context
def export_key(ctx, fingerprint, is_file, is_pvt):
    file_name = None
    passphrase = None

    if is_file is True:
        file_name = click.prompt("Enter the file name", type=str)
        try:
            file_name = Path(file_name)
            file_name.touch(exist_ok=False)
            logging.debug("file not exists.")
        except FileExistsError:
            logging.error("Cause the path already exist, export to file failed.")
            if click.confirm("Do you want to print on console?", default=True):
                is_file = False
            else:
                logging.warning("Mail Client Exit.")
                return

            pass

    if is_pvt is True:
        passphrase = click.prompt(
            "Enter pvt's passphrase", hide_input=True, type=str, default="None"
        )

    pub, pvt = ctx.parent.gpg.export_key(
        fingerprint, export_pvt=is_pvt, password=passphrase
    )

    if pub == "":
        logging.error("The key not exists, please check fingerprint.")
        logging.error("Mail Client Exits.")
        return

    if is_file is False:
        ctx.parent.pp.pprint(pub)
        if is_pvt is True:
            ctx.parent.pp.pprint(pvt)
    else:
        with file_name.open("w") as f:
            f.write(pub)
            if pvt:
                f.write(pvt)

    logging.info("Export key successful.")


@click.command(name="import-key")
@click.option(
    "--file-path",
    "-p",
    prompt="Enter file path",
    required=True,
    type=str,
    help="The path of imported key.",
)
@click.option(
    "--fingerprint",
    "-f",
    prompt="Enter fingerprint",
    required=True,
    callback=check_fingerprint,
    type=str,
    help="The fingerprint of this key/key pair.",
)
@click.pass_context
def import_key(ctx, file_path, fingerprint):
    # scaning key
    res = ctx.parent.gpg.scan_file(file_path)

    if not res:
        logging.error(
            "The file path is wrong. File not found. Or No key (pair) in this file."
        )
        return

    if fingerprint != res[0].get("fingerprint"):
        logging.error(
            "Unsafe Key.\nThe user input fingerprint is different from computed fingerprint."
        )
        logging.error("Mail Client Exits.")
        return

    # import key
    try:
        key_data = Path(file_path).open().read()
        res = ctx.parent.gpg.import_key(key_data=key_data)
    except OSError:
        logging.error("Cannot read the file.")
        return
        pass

    logging.info(
        f"Successful import {res.get('imported')} keys.\nThe fingerprint is:\n{res.get('success')[0].get('fingerprint')}"
    )


client.add_command(create_key)
client.add_command(list_keys)
client.add_command(register)
client.add_command(send)
client.add_command(retrieve)
client.add_command(export_key)
client.add_command(import_key)

if __name__ == "__main__":
    client(prog_name="scmail")
