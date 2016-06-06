# -*- coding: utf-8 -*-
from unittest import TestCase
from nose.tools import ok_, eq_

from rlmanager import IntRingBuffer


class IntRingBufferTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        rb1 = IntRingBuffer(3)

        eq_(3, rb1._size)
        eq_(3, len(rb1._buffer))
        eq_(0, rb1._head)
        eq_(0, rb1._next)
        eq_(0, rb1._count)

    def test_size(self):
        rb1 = IntRingBuffer(3)
        eq_(3, rb1.size)

        rb2 = IntRingBuffer(5)
        eq_(5, rb2.size)

        rb3 = IntRingBuffer(100)
        eq_(100, rb3.size)

    def test_len(self):
        rb1 = IntRingBuffer(3)
        eq_(0, len(rb1))
        rb1.append(10)
        eq_(1, len(rb1))
        rb1.append(20)
        eq_(2, len(rb1))
        rb1.append(30)
        eq_(3, len(rb1))
        rb1.append(40)
        eq_(3, len(rb1))
        rb1.append(50)
        eq_(3, len(rb1))
        rb1.append(60)
        eq_(3, len(rb1))
        rb1.append(70)

        rb2 = IntRingBuffer(5)
        eq_(0, len(rb2))
        for i in xrange(100):
            rb2.append(i * 10)
        eq_(5, len(rb2))

    def test_getitem(self):
        rb1 = IntRingBuffer(3)
        rb1.append(10)
        eq_(10, rb1[0])
        rb1.append(20)
        eq_(10, rb1[0])
        eq_(20, rb1[1])
        rb1.append(30)
        eq_(10, rb1[0])
        eq_(20, rb1[1])
        eq_(30, rb1[2])

        rb1.append(40)
        eq_(20, rb1[0])
        eq_(30, rb1[1])
        eq_(40, rb1[2])

        rb1.append(50)
        eq_(30, rb1[0])
        eq_(40, rb1[1])
        eq_(50, rb1[2])

        rb1.append(60)
        eq_(40, rb1[0])
        eq_(50, rb1[1])
        eq_(60, rb1[2])

        rb1.append(70)
        eq_(50, rb1[0])
        eq_(60, rb1[1])
        eq_(70, rb1[2])

    def test_iter(self):
        rb1 = IntRingBuffer(3)

        rb1.append(10)
        rb1.append(20)
        eq_([10, 20], list(iter(rb1)))

        rb2 = IntRingBuffer(3)
        eq_([], list(iter(rb2)))

        rb3 = IntRingBuffer(3)
        rb3.append(10)
        rb3.append(20)
        rb3.append(30)
        eq_([10, 20, 30], list(iter(rb3)))

        rb4 = IntRingBuffer(3)
        rb4.append(10)
        rb4.append(20)
        rb4.append(30)
        rb4.append(40)
        eq_([20, 30, 40], list(iter(rb4)))

        rb5 = IntRingBuffer(3)
        rb5.append(10)
        rb5.append(20)
        rb5.append(30)
        rb5.append(40)
        rb5.append(50)
        rb5.append(60)
        eq_([40, 50, 60], list(iter(rb5)))

        rb6 = IntRingBuffer(3)
        rb6.append(10)
        rb6.append(20)
        rb6.append(30)
        rb6.append(40)
        rb6.append(50)
        rb6.append(60)
        rb6.append(70)
        eq_([50, 60, 70], list(iter(rb6)))

    def test_popleft(self):
        def _append(rb, numbers):
            for n in numbers:
                rb.append(n)

        rb1 = IntRingBuffer(3)
        eq_(0, len(rb1))
        rb1.append(10)
        eq_(1, len(rb1))
        eq_(10, rb1.popleft())
        eq_(0, len(rb1))
        _append(rb1, [100, 200])
        eq_(2, len(rb1))
        eq_(100, rb1.popleft())
        eq_(1, len(rb1))
        eq_(200, rb1.popleft())
        eq_(0, len(rb1))

        _append(rb1, [100, 200, 300, 400])
        eq_(3, len(rb1))
        eq_(200, rb1.popleft())
        eq_(2, len(rb1))
        eq_(300, rb1.popleft())
        eq_(1, len(rb1))
        eq_(400, rb1.popleft())
        eq_(0, len(rb1))

        _append(rb1, [100, 200, 300, 400, 500, 600, 700])
        eq_(3, len(rb1))
        eq_(500, rb1.popleft())
        eq_(2, len(rb1))
        eq_(600, rb1.popleft())
        eq_(1, len(rb1))
        eq_(700, rb1.popleft())
        eq_(0, len(rb1))

    def test_append(self):
        rb1 = IntRingBuffer(3)

        ok_(rb1._buffer[0] != 10)
        eq_(0, rb1._head)
        eq_(0, rb1._next)
        eq_(0, rb1._count)

        rb1.append(10)

        eq_(0, rb1._head)
        eq_(1, rb1._next)
        eq_(1, rb1._count)

        eq_(10, rb1._buffer[0])

        rb1.append(20)

        eq_(0, rb1._head)
        eq_(2, rb1._next)
        eq_(2, rb1._count)
        eq_(10, rb1._buffer[0])
        eq_(20, rb1._buffer[1])

        rb1.append(30)

        eq_(0, rb1._head)
        eq_(0, rb1._next)
        eq_(3, rb1._count)
        eq_(10, rb1._buffer[0])
        eq_(20, rb1._buffer[1])
        eq_(30, rb1._buffer[2])

        rb1.append(40)

        eq_(1, rb1._head)
        eq_(1, rb1._next)
        eq_(3, rb1._count)
        eq_(40, rb1._buffer[0])
        eq_(20, rb1._buffer[1])
        eq_(30, rb1._buffer[2])

        rb1.append(50)
        eq_(2, rb1._head)
        eq_(2, rb1._next)
        eq_(3, rb1._count)
        eq_(40, rb1._buffer[0])
        eq_(50, rb1._buffer[1])
        eq_(30, rb1._buffer[2])

        rb1.append(60)
        eq_(0, rb1._head)
        eq_(0, rb1._next)
        eq_(3, rb1._count)
        eq_(40, rb1._buffer[0])
        eq_(50, rb1._buffer[1])
        eq_(60, rb1._buffer[2])

        rb1.append(70)
        eq_(1, rb1._head)
        eq_(1, rb1._next)
        eq_(3, rb1._count)
        eq_(70, rb1._buffer[0])
        eq_(50, rb1._buffer[1])
        eq_(60, rb1._buffer[2])
