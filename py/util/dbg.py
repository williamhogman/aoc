def prn(x, *args, **kwargs):
    print(x, *args, dict(kwargs))
    return x
