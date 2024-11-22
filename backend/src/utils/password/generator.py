import secrets
import string


def generate(length: int):
    if length < 4:
        raise ValueError("Password length must be at least 4 to include all character types.")

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    # special_chars = string.punctuation

    all_characters = lowercase + uppercase + digits
    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        # secrets.choice(special_chars)
    ]

    password += [secrets.choice(all_characters) for _ in range(length - 4)]
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)
