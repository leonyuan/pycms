from os.path import abspath, dirname, join
from web.contrib.template import render_mako


curdir = abspath(dirname(__file__))

render = render_mako(
            directories=[join(curdir, '../templates/blog/')],
            input_encoding='utf-8',
            output_encoding='utf-8',
         )


