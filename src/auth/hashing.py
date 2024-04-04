from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated = "auto")

def get_hashed_password(password: str):
    hash_pwd = pwd_cxt.hash(password)
    return hash_pwd


def verify_hash_password(plain_password, hash_password):
    decode_pwd = pwd_cxt.verify(plain_password, hash_password)
    return decode_pwd