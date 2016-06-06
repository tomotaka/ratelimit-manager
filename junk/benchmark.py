# -*- coding: utf-8 -*-
import numpy as np
import bisect
import time
import random


def linear_insertion_point_finder(array, v):
    for i, av in enumerate(array):
        if v < av:
            return i
    return len(array)


def main():
    LEN = 100000
    N = 5000

    candidates = [234, 5678, 0, 20000, 1435, 7640, 2750, 9621]

    buffer = np.ndarray((LEN,), dtype=np.int64)
    for i in xrange(LEN):
        buffer[i] = random.random() * 10000
    print 'initialized'

    t1 = time.time()
    for _ in xrange(N):
        for n in candidates:
            np.searchsorted(buffer, n)
    t2 = time.time()
    print 'numpy: %.4fsec' % (t2 - t1)

    t1 = time.time()
    for _ in xrange(N):
        for n in candidates:
            bisect.bisect_left(buffer, n)
    t2 = time.time()
    print 'bisect: %.4fsec' % (t2 - t1)

    t1 = time.time()
    for _ in xrange(N):
        for n in candidates:
            # bisect.bisect_left(buffer, n)
            linear_insertion_point_finder(buffer, n)
    t2 = time.time()
    print 'linear: %.4fsec' % (t2 - t1)


if __name__ == '__main__':
    main()
