#! /usr/bin/env python3
""" Secure Password Generator """

import argparse
import secrets
import string

# Password Generation Constants
PASSWORD_LENGTH = 16
POOL = string.ascii_letters + string.digits + string.punctuation
POOL = ''.join(c for c in POOL if c not in '$,"\'')

def main():
    """ Secure Password Generator """

    parser = argparse.ArgumentParser(
        description="Generates cryptographically strong random passwords",
        epilog="""Note: Passwords may contain ambiguous characters such as
        $, ,, ', and ". If you prefer passwords that do not contain these characters, try the -p flag."""
    )

    parser.add_argument(
        "-l", "--length",
        action="store",
        type=int,
        metavar="LENGTH",
        default=PASSWORD_LENGTH,
        help="Specify password length (default: %(default)s)"
    )

    args = parser.parse_args()

    if args.length < 8:
        raise ValueError("Password length must be at least 8 characters")

    password = ''.join(secrets.choice(POOL) for i in range(args.length))
    print(password)

if __name__ == "__main__":
    main()

