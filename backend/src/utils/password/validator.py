import bcrypt


def match(first: str, second: str) -> bool:
    return bcrypt.checkpw(first.encode('utf-8'), second.encode('utf-8'))


def hash_secret(secret: str) -> str:
    return bcrypt.hashpw(secret.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
