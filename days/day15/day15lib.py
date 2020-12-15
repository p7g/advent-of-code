from collections import defaultdict, deque
from itertools import count


def go(data, nth):
    seen = defaultdict(lambda: deque(maxlen=2))
    prev = None
    len_ = len
    datalen = len(data)
    for i in count():
        if i == nth:
            return prev
        if i < datalen:
            prev = data[i]
        elif len_(seen[prev]) == 1:
            prev = 0
        else:
            prev = seen[prev][0] - seen[prev][1]
        seen[prev].appendleft(i)
