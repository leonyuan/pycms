import web
from hashlib import sha1


def get_hexdigest(salt, raw_password):
    return sha1(salt + raw_password).hexdigest()

def check_password(raw_password, enc_password):
    salt, hsh = enc_password.split('$')
    return hsh == get_hexdigest(salt, raw_password)
