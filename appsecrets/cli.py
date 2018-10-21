import argparse
import sys

from .api import Secrets
from .exc import Error


def encrypt(args: argparse.Namespace) -> None:
    Secrets(args.path).encrypt_all()
    print("Secrets in %s are now all encrypted" % args.path)


def decrypt(args: argparse.Namespace) -> None:
    plaintext = Secrets(args.path).decrypt(name=args.name)
    print(plaintext.decode('utf-8'), end='')


def check(args: argparse.Namespace) -> None:
    names = Secrets(args.path).list_unencrypted()
    if len(names) > 0:
        print("Error: secrets in plaintext: %s" % ', '.join(names))
        sys.exit(1)


def create(args: argparse.Namespace) -> None:
    Secrets.create(args.path, key_id=args.google_kms)

    print(f"""

        You can now add a secret with:

            $ echo -n 'SOMESECRETDATA' > {args.path}/my-secret-name
            $ appsecrets encrypt {args.path}

    """)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='command')

    sp = subparsers.add_parser('create', help='Create a appsecrets store')
    sp.add_argument('path')
    sp.add_argument('--google-kms', type=str, required=True, help='The Google KMS key resource id to use')
    sp.set_defaults(func=create)

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


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)

    try:
        args.func(args)
    except Error as err:
        sys.exit(err)
