#encoding=utf-8
import web
from web import config as cfg
from sqlalchemy import func


def paging(pno, pnum):
    pl = []
    pl.extend(range(1, (pnum > 2 and 2 or pnum)+1))
    pl.extend(range(pnum-1, pnum+1))
    pl.extend(range(pno-2, pno+3))
    for i in range(len(pl)-1,-1,-1):
        if pl[i] < 1 or pl[i] > pnum:
            del pl[i]

    uniqs = set()
    pl2 = []
    for p in pl:
        if p in uniqs:
            continue
        uniqs.add(p)
        pl2.append(p)

    pl2.sort()

    if len(pl2) > 4:
        if pl2[2] > pl2[1]+1:
            pl2.insert(2, 0)
        if pl2[-3]+1 < pl2[-2]:
            pl2.insert(-2, 0)

    return pl2

class Pagination(object):
    def __init__(self, record_query, count_query, pno=1, psize=cfg.default_page_size):
        self.pno = int(pno)
        self.psize = psize
        self.recnum = 0
        self.pnum = 0
        self.record_query = record_query
        self.count_query = count_query
        self._queryset = None
        self._paginations = None

    @property
    def queryset(self):
        if self._queryset is None:
            offset = (self.pno-1) * self.psize
            self.recnum = self.count_query.count()
            self.pnum = self.recnum / self.psize + (self.recnum % self.psize > 0 and 1 or 0)
            self._queryset = self.record_query.offset(offset).limit(self.psize)
        return self._queryset

    @property
    def paginations(self):
        if self._paginations is None:
            self._pagination = paging(self.pno, self.pnum)
        return self._pagination


