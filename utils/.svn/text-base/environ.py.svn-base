import web


def setup_config(cfgmod):
    for item in dir(cfgmod):
        item_val = getattr(cfgmod, item)
        setattr(web.config, item, item_val)

