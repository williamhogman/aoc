import re

from fastcore.all import store_attr, L, tuplify, detuplify, Self
from .io import read
from .ds import Table

def maybe_number(x, ints):
    if not ints:
        return x

    if x.isnumeric():
        return int(x)
    try:
        if "." in x:
            return float(x)
    except:
        pass
    return x

def prn(x):
    print(x)
    return x

class Parser:
    def __init__(self, line_sep="\n", field_sep=r"(?:[\,:\-]\s*)|(?:\s+)", ints=True, skip_last=True):
        store_attr()

    def __call__(self, data: str):
        l_re = re.compile(self.line_sep)
        ls = L(l_re.split(data))
        fs_re = re.compile(self.field_sep)
        r = L(ls).map(fs_re.split).map(L).map(Self.map(maybe_number, ints=self.ints))[:-1]
        return Table(r)


class Exercise:
    def __init__(self, day, year=2020, reader=read, parser={}):
        self.f_reader = (lambda x: x)
        self.fn_part1 = {}
        self.fn_part2 = {}
        self.f_reader = reader
        self.f_parser = parser
        self.f_transformer = (lambda x: x)
        store_attr(but='reader,parser')

    def reader(self, f):
        self.f_reader = f
        return f

    def loader(self, f):
        self.f_loader = f
        return f

    def transformer(self, f):
        self.f_transformer = f
        return f

    def _deco_fn(self, f, map=False, reduce=None):
        if not map:
            return f
        else:
            def _inner(x):
                mapped = x.map(f)
                if reduce == "sum":
                    return mapped.t.reduce(lambda a, b: a + b)
                elif reduce == "prod":
                    return mapped.t.reduce(lambda a, b: a * b)
                elif reduce == "count":
                    return len(mapped.t.map(lambda x: x[0]).filter(lambda x: x))
                elif callable(f):
                    return mapped.t.reduce(f)
                elif reduce is None:
                    return mapped
            return _inner


    def _add_fn(self, target, f, n: str = "default", **kwargs):
        if n in target:
            i = 2
            orig_n = n
            while n in target:
                n = f"{orig_n}_{i}"
                n += 1
        target[n] = self._deco_fn(f, **kwargs)

    def _deco(self, target, *args, **kwargs):
        def inner(f):
            self._add_fn(target, f, *args, **kwargs)
            return f
        if len(args) == 1 and callable(args[0]):
            return inner(args[0])
        else:
            return inner

    def part1(self, *args, **kwargs):
        return self._deco(self.fn_part1, *args, **kwargs)

    def part2(self, *args, **kwargs):
        return self._deco(self.fn_part2, *args, **kwargs)

    def _call_all(self, target, data):
        results = {}
        for k, v in target.items():
            print(f"Running {k}")
            res = v(data)
            results[k] = res

        if len(results) == 1:
            for k in results:
                print(results[k])
        elif results:
            print(results)

    def __call__(self):
        data = self.f_reader(self.day)
        parser = (
            Parser(**self.f_parser)
            if isinstance(self.f_parser, dict)
            else self.f_parser
        )
        parsed = parser(data)
        transformed = self.f_transformer(parsed)

        for part in [self.fn_part1, self.fn_part2]:
            self._call_all(part, transformed)
