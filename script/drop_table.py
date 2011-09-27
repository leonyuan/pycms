#!/bin/env python
from common import Base, engine
from account.model import metadata as account_metadata
from blog.model import metadata as blog_metadata


if __name__ == '__main__':
    account_metadata.drop_all(engine)
    blog_metadata.drop_all(engine)
