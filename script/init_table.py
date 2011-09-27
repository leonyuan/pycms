#!/bin/env python
from common import Base, engine
from account.model import *
from blog.model import *
from model.model import *

import init_perm_data, init_user_data, init_template_data, init_category_data


if __name__ == '__main__':
    metadata.create_all(engine)

    init_perm_data.init()
    init_user_data.init()
    init_template_data.init()
    init_category_data.init()
