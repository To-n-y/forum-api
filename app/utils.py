import hashlib
from app.config import SECRET_KEY


def get_hash_password(password: str) -> str:
    return hashlib.sha256(f"{SECRET_KEY}{password}".encode("utf8")).hexdigest()
