def one(n):
    yield n


def fwd(bs):
    bs = list(bs)
    x = yield
    try:
        while True:
            for b in bs:
                x = b.send(x)
            x = yield x
    except StopIteration:
        return x


def pipe(a, b):
    for x in a:
        yield b.send(x)
