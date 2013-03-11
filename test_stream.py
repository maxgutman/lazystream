#!/usr/bin/env python

"""Test the implementation of the stream class"""

__author__ = 'Max Gutman'
__email__ = 'mxgutman@gmail.com'
__python_version = '2.7.1'


import threading
import time
import unittest
from stream import *

class TestStreamFunctions(unittest.TestCase):

    PRIME_NUMBERS = (2,3,5,7,11,13,17,19,23,29, 31,37,41,43,47,53,59,61,67,71,
        73,79,83,89,97,101,103,107,109,113, 127,131,137,139,149,151,157,163,
        167,173, 179,181,191,193,197,199,211,223,227,229, 233,239,241,251,257)

    def test_stream_popnext(self):
        """PopNext"""
        stream = Counters(5)
        for i in xrange(5, 10):
            self.assertEqual(i, stream.popNext())

    def test_stream_popn(self):
        """PopN"""
        stream = Counters()
        self.assertEqual(range(5), list(stream.popN(5)))

    def test_stream_randoms(self, num_iterations=250):
        """Randoms"""
        numbers = []
        stream = Randoms(max=num_iterations)
        for n in range(num_iterations):
            next = stream.popNext()
            self.assertTrue(next not in numbers)
            self.assertTrue(isinstance(next, long))
            numbers.append(next)

    def test_stream_primes(self):
        """Primes"""
        stream = Primes(max=len(self.PRIME_NUMBERS))
        for prime_number in self.PRIME_NUMBERS:
            next = stream.popNext()
            self.assertEqual(prime_number, next)

    def test_stream_primefactors(self, n=255, expected=[3, 5, 17]):
        """PrimeFactors"""
        PRIME_NUMBERS = []
        stream = PrimeFactors(n)
        next = stream.popNext()
        while next:
            PRIME_NUMBERS.append(next)
            next = stream.popNext()
        self.assertEqual(expected, PRIME_NUMBERS)

    def test_high_order_map(self):
        """Map"""
        _map = ['_2_','_3_','_5_','_7_','_11_']
        _map_actual = list(map(lambda x: '_%s_' % x, Primes(5)))
        #print _map_actual
        self.assertEqual(_map, _map_actual)

    def test_high_order_filter(self):
        """Filter"""
        _filter = [17, 19, 23, 29]
        _filter_actual = list(filter(lambda x: x > 13, Primes(10)))
        #print _filter_actual
        self.assertEqual(_filter, _filter_actual)

    def test_high_order_zip_with(self):
        """ZipWith"""
        _zip = [(2, 1), (3, 2), (5, 3), (7, 4), (11, 5)]
        _zip_actual = list(zipWith(lambda x, y: (x, y), Primes(5), Counters(1)))
        #print _zip_actual
        self.assertEqual(_zip, _zip_actual)

    def test_high_order_prefix_reduce(self):
        """PrefixReduce"""
        _reduce = [(0, 2), ((0, 2), 3), (((0, 2), 3), 5)]
        _reduce_actual = list(prefixReduce(lambda x, y: (x, y), Primes(3), 0))
        #print _reduce_actual
        self.assertEqual(_reduce, _reduce_actual)


def run_sequential(fn, n=100000):
    """Returns timing of n executions of function fn done sequentially"""
    import time

    def _test_fn(n=100000):
        for _ in xrange(n):
            fn()
    start = time.time()
    _test_fn()
    return time.time() - start

def run_threading(fn):
    """Returns timing of n executions of function fn done in two threads"""
    import time
    import threading

    def _test_fn(n=100000):
        for _ in xrange(n):
            fn()

    thread1 = threading.Thread(target=_test_fn)
    thread2 = threading.Thread(target=_test_fn)
    start = time.time()
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    return time.time() - start

def main():
    unittest.main()
    tests = TestStreamFunctions()
    print run_sequential(fn=tests.test_high_order_map)
    print run_threading(fn=tests.test_high_order_map)

if __name__ == "__main__":
    main()
