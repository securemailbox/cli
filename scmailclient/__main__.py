# from ..scmailclient.scmail import main as client
import sys
sys.path.append('../')
from scmailclient import main as client


def main():
    """Launch the command line program."""
    client()


if __name__ == '__main__':
    main()

