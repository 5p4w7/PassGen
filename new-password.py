"""Small secure password generator.

Preserves original behavior: password starts with a letter and excludes
$, comma, single- and double-quote characters.
"""
from typing import Sequence
import argparse
import secrets
import string

# Characters to exclude from the password
FORBIDDEN_CHARS = {"$", ",", "'", '"'}


def _build_allowed_chars() -> str:
    """Return the allowed character set as a string (letters, digits, punctuation minus forbidden)."""
    pool = string.ascii_letters + string.digits + string.punctuation
    return ''.join(ch for ch in pool if ch not in FORBIDDEN_CHARS)


def generate_password(length: int) -> str:
    """Generate a random password.

    The first character is always an ASCII letter. Remaining characters are
    chosen from allowed characters (letters, digits, punctuation with some
    forbidden symbols removed).

    Raises:
        ValueError: if length is not a positive integer.
    """
    if not isinstance(length, int) or length <= 0:
        raise ValueError("length must be a positive integer")

    allowed = _build_allowed_chars()
    if not allowed:
        raise RuntimeError("No allowed characters available to build password")

    # First character must be a letter per original requirement
    first_char = secrets.choice(string.ascii_letters)

    # Use a list comprehension for clarity and slightly better performance
    rest = [secrets.choice(allowed) for _ in range(length - 1)]
    return ''.join([first_char] + rest)


def _prompt_for_length() -> int:
    while True:
        try:
            value = int(input("Enter the desired password length: "))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Generate a secure password.")
    parser.add_argument('-l', '--length', type=int, help='Password length')
    args = parser.parse_args(argv)

    if args.length is None:
        length = _prompt_for_length()
    else:
        length = args.length

    password = generate_password(length)
    print(f"Generated password: {password}")


if __name__ == '__main__':
    main()
