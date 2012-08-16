import os.path
from web import config as cfg
from pycms.utils.render import render_mako

admin_render = render_mako(
            directories=[os.path.join(cfg.admin_template_dir, 'category'), cfg.admin_template_dir],
            input_encoding='utf-8',
            output_encoding='utf-8',
         )

