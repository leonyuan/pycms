import web
from hashlib import sha1


class LazyUser(object):
    def __get__(self, obj, objtype):
        from account.auth import get_logined_user
        return get_logined_user()

def get_hexdigest(salt, raw_password):
    return sha1(salt + raw_password).hexdigest()

def check_password(raw_password, enc_password):
    salt, hsh = enc_password.split('$')
    return hsh == get_hexdigest(salt, raw_password)
