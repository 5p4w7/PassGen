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

def generate_password(length: int, exclude_ambiguous: bool = False) -> str:
    """Generate a secure password with guaranteed diversity.

    If `exclude_ambiguous` is True, characters in `FORBIDDEN_CHARS` are omitted
    from the punctuation pool.
    """
    if length < MIN_LENGTH:
        raise ValueError(f"Length must be >= {MIN_LENGTH}")

    # Build pools depending on the ambiguous-character preference
    letters = _LETTERS
    digits = _DIGITS
    punctuation = ''.join(ch for ch in string.punctuation if not (exclude_ambiguous and ch in FORBIDDEN_CHARS))
    all_pool = letters + digits + punctuation

    # Ensure punctuation pool is non-empty (defensive)
    if not punctuation:
        # fallback to a minimal punctuation set if everything was filtered
        punctuation = '!@#%&*()-_=+[]{};:<>/?'
        all_pool = letters + digits + punctuation

    # Start with mandatory diversity: 1 letter, 1 digit, 1 punctuation
    password = [
        secrets.choice(letters),
        secrets.choice(digits),
        secrets.choice(punctuation),
    ]

    # Fill the rest of the password
    password += [secrets.choice(all_pool) for _ in range(length - 3)]

    # Shuffle to ensure the forced characters aren't always at the start
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)

def _prompt_for_length() -> int:
    while True:
        try:
            raw = input(f"Enter password length (min {MIN_LENGTH}): ").strip()
            if not raw:
                print("Please enter a value.")
                continue
            ivalue = int(raw)
            if ivalue < MIN_LENGTH:
                print(f"Length must be at least {MIN_LENGTH}.")
                continue
            return ivalue
        except ValueError:
            print("Invalid integer.")
        except KeyboardInterrupt:
            raise SystemExit("\nCancelled.")

def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Generate a secure password.")
    parser.add_argument('-l', '--length', type=_positive_int, help='Password length')
    parser.add_argument('-p', '--prune', action='store_true',
                        help='Exclude ambiguous characters ($ , \" \') from the password')
    args = parser.parse_args(argv)

    length = args.length or _prompt_for_length()
    print(f"Generated password: {generate_password(length, exclude_ambiguous=bool(args.prune))}")

if __name__ == '__main__':
    main()