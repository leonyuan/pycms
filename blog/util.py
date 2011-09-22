from web.contrib.template import render_mako


render = render_mako(
            directories=['templates/blog/'],
            input_encoding='utf-8',
            output_encoding='utf-8',
         )


