from common.util import render_mako
from common.config import template_dir


render = render_mako(
            directories=[template_dir+'basis/'],
            input_encoding='utf-8',
            output_encoding='utf-8',
         )


