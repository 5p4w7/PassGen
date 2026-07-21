# Secure Password Generator

This small script generates cryptographically-strong random passwords.

Usage
-----

Run the script interactively (it will prompt for a length if you omit `-l`):

    python new-password.py

Or supply a length on the command line:

    python new-password.py -l 12

Flags
-----

- `-l`, `--length` : Specify the password length (minimum 8).

- `-p`, `--prune` : Exclude ambiguous punctuation characters (`$`, `,`, `'`, `"`).

Examples
--------

Generate a 16-character password (interactive prompt or default):

    python new-password.py

Generate a 12-character password:

    python new-password.py -l 12

Generate a 12-character password without ambiguous punctuation:

    python new-password.py -l 12 -p

Notes
-----

- The interactive prompt now validates input and will politely re-prompt for values below the minimum.
- The previous README contained an older script and mentioned a `-p` flag which is not implemented in the current script; this README reflects the current behaviour.

License
-------

MIT-style — feel free to adapt for your needs.


