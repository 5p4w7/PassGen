"""Small secure password generator.

Preserves original behavior: password starts with a letter and excludes
$, comma, single- and double-quote characters.
"""
import argparse
import secrets
import string
from typing import Sequence

# Characters to exclude from the password
FORBIDDEN_CHARS: frozenset[str] = frozenset({"$", ",", "'", '"'})

# Minimum sensible password length
MIN_LENGTH = 8

# Build the allowed character pool once at import time
_ALLOWED_CHARS: str = ''.join(
    ch for ch in (string.ascii_letters + string.digits + string.punctuation)
    if ch not in FORBIDDEN_CHARS
)


def _positive_int(value: str) -> int:
    """argparse type: parse a positive integer >= MIN_LENGTH, else raise ArgumentTypeError."""
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value!r} is not a valid integer")
    if ivalue < MIN_LENGTH:
        raise argparse.ArgumentTypeError(
            f"Password length must be at least {MIN_LENGTH}, got {ivalue}"
        )
    return ivalue


def generate_password(length: int) -> str:
    """Generate a cryptographically secure random password.

    The first character is always an ASCII letter. Remaining characters are
    chosen from the allowed set (letters, digits, punctuation minus forbidden).

    Args:
        length: Total password length; must be >= MIN_LENGTH.

    Raises:
        ValueError: if length is less than MIN_LENGTH.
    """
    if not isinstance(length, int) or length < MIN_LENGTH:
        raise ValueError(f"length must be an integer >= {MIN_LENGTH}, got {length!r}")

    if not _ALLOWED_CHARS:
        raise RuntimeError("No allowed characters available to build password")

    first_char = secrets.choice(string.ascii_letters)
    rest = [secrets.choice(_ALLOWED_CHARS) for _ in range(length - 1)]
    return first_char + ''.join(rest)


def _prompt_for_length() -> int:
    """Interactively prompt the user for a valid password length."""
    while True:
        try:
            raw = input(f"Enter the desired password length (min {MIN_LENGTH}): ")
            value = int(raw)
            if value < MIN_LENGTH:
                print(f"Please enter a number >= {MIN_LENGTH}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
        except KeyboardInterrupt:
            print("\nCancelled.")
            raise SystemExit(0)


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Generate a secure password.")
    parser.add_argument(
        '-l', '--length',
        type=_positive_int,
        metavar='N',
        help=f'Password length (minimum {MIN_LENGTH})',
    )
    args = parser.parse_args(argv)

    length = args.length if args.length is not None else _prompt_for_length()
    password = generate_password(length)
    print(f"Generated password: {password}")


if __name__ == '__main__':
    main()
