import argparse
import secrets
import string
from typing import Sequence

# Characters to exclude from the password
FORBIDDEN_CHARS: frozenset[str] = frozenset({"$", ",", "'", '"'})
MIN_LENGTH = 8

# Build pools for guaranteed inclusion
_LETTERS = string.ascii_letters
_DIGITS = string.digits
_PUNCTUATION = ''.join(ch for ch in string.punctuation if ch not in FORBIDDEN_CHARS)
_ALL_POOL = _LETTERS + _DIGITS + _PUNCTUATION

def _positive_int(value: str) -> int:
    """argparse type: parse a positive integer >= MIN_LENGTH."""
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value!r} is not a valid integer")
    if ivalue < MIN_LENGTH:
        raise argparse.ArgumentTypeError(f"Length must be at least {MIN_LENGTH}")
    return ivalue

def generate_password(length: int) -> str:
    """Generate a secure password with guaranteed diversity."""
    if length < MIN_LENGTH:
        raise ValueError(f"Length must be >= {MIN_LENGTH}")

    # Start with mandatory diversity: 1 letter, 1 digit, 1 punctuation
    password = [
        secrets.choice(_LETTERS),
        secrets.choice(_DIGITS),
        secrets.choice(_PUNCTUATION),
    ]

    # Fill the rest of the password
    password += [secrets.choice(_ALL_POOL) for _ in range(length - 3)]

    # Shuffle to ensure the forced characters aren't always at the start
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)

def _prompt_for_length() -> int:
    while True:
        try:
            return int(input(f"Enter password length (min {MIN_LENGTH}): "))
        except ValueError:
            print("Invalid integer.")
        except KeyboardInterrupt:
            raise SystemExit("\nCancelled.")

def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Generate a secure password.")
    parser.add_argument('-l', '--length', type=_positive_int, help='Password length')
    args = parser.parse_args(argv)

    length = args.length or _prompt_for_length()
    print(f"Generated password: {generate_password(length)}")

if __name__ == '__main__':
    main()