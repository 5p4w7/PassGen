# PassGen

A simple Python password generator that creates strong, varied passwords with optional exclusion of ambiguous characters.

## Features

- Generates secure passwords using Python's `secrets` module
- Enforces at least one letter, one digit, and one punctuation character
- Supports optional exclusion of ambiguous punctuation such as `$`, `,`, `'`, and `"`
- Includes a small command-line interface for easy use

## Usage

Run the script interactively:

```bash
python new-password.py
```

Or supply a length on the command line:

```bash
python new-password.py -l 12
```

Optional flag:

```bash
python new-password.py -l 12 -p
```

## Requirements

- Python 3.9+

## License

MIT-style — feel free to adapt for your needs.

-END-