from passlib.context import CryptContext

# Use pbkdf2_sha256 to avoid bcrypt's 72-byte limit and external bcrypt dependency
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def _truncate_to_72(password: str) -> str:
    """Truncate a password to 72 bytes (bcrypt limit) preserving UTF-8."""
    if password is None:
        return ""
    b = password.encode("utf-8")
    if len(b) <= 72:
        return password
    tb = b[:72]
    return tb.decode("utf-8", errors="ignore")


def hash_password(password: str) -> str:
    pw = _truncate_to_72(password)
    return pwd_context.hash(pw)


def verify_password(plain: str, hashed: str) -> bool:
    pw = _truncate_to_72(plain)
    return pwd_context.verify(pw, hashed)