#!/usr/bin/env python

"""Implement a Stream class using built-ins"""

__author__ = 'Max Gutman'
__email__ = 'mxgutman@gmail.com'
__python_version = '2.7.1'


class Stream(object):

    def __init__(self, max=None):
        self.current = 0
        # Stop iteration at "max"
        self.max = max
        self._iter = self.__iter__()

    def popNext(self):
        """Returns the next element of the stream, if any, otherwise None."""
        if self.max and self.current > self.max - 1:
            return None
        else:
            self.current += 1
            try:
                return self._iter.next()
            except StopIteration:
                return None

    def popN(self, num):
        """Returns up to num elements from the stream"""
        # import ipdb; ipdb.set_trace()
        return (self.popNext() for n in range(num))


class Counters(Stream):
    """Returns a stream counter (used for testing)"""

    def __init__(self, start=0, **kwargs):
        super(Counters, self).__init__(**kwargs)
        self.start = start

    def __iter__(self):
        num = self.start
        while True:
            yield num
            num += 1


class Randoms(Stream):
    """Returns a random stream of unique random numbers."""

    def __iter__(self):
        """Recursively generates png's and uses new png to re-seed.
        This is the technique for generating linear congruential numbers.
        """
        random = self.psuedo_random()
        while True:
            yield random
            random = self.psuedo_random(random)

    def psuedo_random(self, seed=0):
        """Return a psuedorandom number"""
        modulo = 2**64
        multiplier = 6364136223846793005
        constant = 2*32
        return (multiplier * seed + constant) % modulo


class Primes(Stream):
    """Returns a stream of ordered prime numbers."""

    def __iter__(self):
        num = 2
        yield num
        while True:
            num += 1
            if self.is_prime(num):
                yield num

    def is_prime(self, num):
        if num < 2:
            return False
        for n in range(2, num):
            if num % n == 0:
                return False
        return True


class PrimeFactors(Stream):
    """Returns a stream of prime factors for a given integer."""

    def __init__(self, num, **kwargs):
        super(PrimeFactors, self).__init__(**kwargs)
        self.num = num

    def __iter__(self):
        x = 2
        while x <= self.num:
            if self.num % x == 0:
                self.num /= x
                yield x
            else:
                x += 1


def map(fn, stream):
    """Returns a stream where fn has been applied to each element."""
    next = stream.popNext()
    while next:
        yield fn(next)
        next = stream.popNext()

def filter(fn, stream):
    """Returns a stream containing only the elements of the stream
    for which fn returns True.
    """
    next = stream.popNext()
    while next:
        if fn(next):
            yield next
        next = stream.popNext()


def zipWith(fn, streamA, streamB):
    """Applies a given binary function pairwise to the elements
    of two given lists.
    """
    nextA = streamA.popNext()
    nextB = streamB.popNext()
    while nextA and nextB:
        yield fn(nextA, nextB)
        nextA = streamA.popNext()
        nextB = streamB.popNext()


def prefixReduce(fn, stream, init=None):
    """Where fn(x,y) is a function to perform a reduction across the stream,
    returns a stream where the nth element is the result of combining the
    first n elements of the input stream using fn."""
    y = init
    next = stream.popNext()
    while next:
        y = fn(y, next)
        yield y
        next = stream.popNext()

