import os.path
import web
from web import config as cfg
from hashlib import sha1
from pycms.utils.render import render_mako


render = render_mako(
            directories=[os.path.join(cfg.template_dir, 'account')],
            input_encoding='utf-8',
            output_encoding='utf-8',
         )

admin_render = render_mako(
            directories=[os.path.join(cfg.admin_template_dir, 'account'), cfg.admin_template_dir],
            input_encoding='utf-8',
            output_encoding='utf-8',
         )

class LazyUser(object):
    def __get__(self, obj, objtype):
        from pycms.account.auth import get_logined_user
        return get_logined_user()

def get_hexdigest(salt, raw_password):
    return sha1(salt + raw_password).hexdigest()

def check_password(raw_password, enc_password):
    salt, hsh = enc_password.split('$')
    return hsh == get_hexdigest(salt, raw_password)
