import jwt
from datetime import datetime, timedelta
import bcrypt

ACCESS_SECRET = "ACCESS_SECRET_KEY_CHANGE_THIS"
REFRESH_SECRET = "REFRESH_SECRET_KEY_CHANGE_THIS"
ALGORITHM = "HS256"

ACCESS_EXPIRE_MINUTES = 30
REFRESH_EXPIRE_DAYS = 30

# ----------------------------
# PASSWORD HASHING
# ----------------------------
def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain: str, hashed: str) -> bool:
    plain_bytes = plain.encode('utf-8')
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(plain_bytes, hashed_bytes)


# ----------------------------
# TOKEN CREATION
# ----------------------------
def create_access_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    return jwt.encode(payload, ACCESS_SECRET, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(days=REFRESH_EXPIRE_DAYS)
    return jwt.encode(payload, REFRESH_SECRET, algorithm=ALGORITHM)


# ----------------------------
# TOKEN DECODING (MISSING in your file)
# ----------------------------
def decode_token(token: str, refresh: bool = False):
    try:
        secret = REFRESH_SECRET if refresh else ACCESS_SECRET
        decoded = jwt.decode(token, secret, algorithms=[ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
