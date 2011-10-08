#!/bin/env python
from common import Base, engine
from account.model import *
from basis.model import *
from models.model import *


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        metadata.create_all(engine)
    elif sys.argv[1].lower() == 'drop':
        metadata.drop_all(engine)

