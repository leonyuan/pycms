from web.contrib.template import render_mako as _render_mako


class render_mako(_render_mako):
    def render(self, filename, **kwargs):
        t = self._lookup.get_template(filename)
        return t.render(**kwargs)


