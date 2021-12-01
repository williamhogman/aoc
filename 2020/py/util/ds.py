import requests
import re
from fastcore.all import listify, L, tuplify, Self


class Table:
    def __init__(self, x, raw=False):
        if raw:
            self.t = x
        else:
            self.t = L(map(tuplify, x))


    def count_where(self, x):
        return len(self.t.filter(x))

    def __repr__(self):
        return f"Table({self.t})"

    def __len__(self):
        return len(self.t)

    def col(self, n=0):
        return self.t.map(Self[n])

    def map(self, *args, **kwargs):
        return Table(self.t.map(*args, **kwargs), raw=True)

    def reduce(self, *args, **kwargs):
        return Table(self.t.reduce(*args, **kwargs), raw=True)

    def filter(self, *args, **kwargs):
        return Table(self.t.filter(*args, **kwargs), raw=True)
