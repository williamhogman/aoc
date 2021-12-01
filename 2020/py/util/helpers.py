import re


def between(x, mn, mx):
    if isinstance(x, str):
        try:
            x = int(x)
        except:
            x = float(x)
    return x >= mn and mx >= x

int_re = re.compile("\d+")
word_re = re.compile("\w+")
def force_int(x):
    if not x:
        return None
    elif isinstance(x, int) or isinstance(x, float):
        x = str(x)
    m = int_re.match(x).group(0)
    if m:
        return int(m)
    else:
        return None

def sigil(x):
    return word_re.match(x).groups()
