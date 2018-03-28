import argparse
import sys

from .api import Secrets
from .exc import Error


def encrypt(args):
    Secrets(args.path).encrypt_all()
    print("Secrets in %s are now all encrypted" % args.path)


def decrypt(args):
    plaintext = Secrets(args.path).decrypt(name=args.name)
    print(plaintext.decode('utf-8'), end='')


def check(args):
    names = Secrets(args.path).list_unencrypted()
    if names:
        print("Error: secrets in plaintext: %s" % ', '.join(names))
        sys.exit(1)


def build_parser():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='command')

    sp = subparsers.add_parser('encrypt', help='Encrypt all secrets in plaintext')
    sp.add_argument('path')
    sp.set_defaults(func=encrypt)

    sp = subparsers.add_parser('decrypt', help='Decrypt a secret and print to stdout')
    sp.add_argument('path')
    sp.add_argument('name')
    sp.set_defaults(func=decrypt)

    sp = subparsers.add_parser('check', help='Succeed only if all secrets are encrypted')
    sp.add_argument('path')
    sp.set_defaults(func=check)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)

    try:
        args.func(args)
    except Error as err:
        sys.exit(err)

    # if args.command == 'encrypt':
    #     Secrets(args.path).encrypt_all()

    # elif args.command == 'decrypt':
    #     Secrets(args.path).decrypt(name=args.secret_name)

    # elif args.command == 'check-unencrypted':
    #     Secrets(args.path).check_unencrypted()
