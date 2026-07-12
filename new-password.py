import secrets
import string

def generate_password(length):
    """Generate a random password that starts with a letter
    and avoids $, commas, and quotation marks."""

    if length <= 0:
        raise ValueError("Password length must be positive")

    # Start with a letter, then continue with safe characters
    first_char = secrets.choice(string.ascii_letters)
    allowed_chars = string.ascii_letters + string.digits
    allowed_chars += "".join(
        ch for ch in string.punctuation if ch not in "$,'\" "
    )

    password_chars = [first_char]
    password_chars.extend(secrets.choice(allowed_chars) for _ in range(length - 1))

    return "".join(password_chars)

# Ask user for password length
while True:
    try:
        length = int(input("Enter the desired password length: "))
        if length <= 0:
            print("Please enter a positive number.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

# Generate and display the password
password = generate_password(length)
print(f"Generated password: {password}")
