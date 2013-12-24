lazystream
==========

A lazy stream implementation in python using only built-ins.


challenge
=========
Complete the following programming challenge using only python built-ins and without help.
One way of imagining a lazy stream implementation in python is any class that implements the method: popNext() which returns the next element of the stream, if any, otherwise None.

1. Write the following classes that implement popNext() and be sure to implement each lazily:
  
  i) Randoms - returns a random stream of unique random numbers 
  
  ii) Primes - returns a stream of ordered prime numbers
  
  iii) PrimeFactors - returns a stream of prime factors for a given integer 

2. Implement the following higher-order functions to test your classes: 

    map(fn, stream) # Returns a stream where fn has been applied to each element. 

    filter(fn, stream) # Returns a stream containing only the elements of the stream for which fn returns True. 

    zipWith(fn, streamA, streamB) # Applies a given binary function pairwise to the elements of two given lists.

    prefixReduce(fn, stream, init) # Where fn(x,y) is a function to perform a reduction across the stream, returns a stream where the nth element is the result of combining the first n elements of the input stream using fn.

3. Add the method: 

  popN(num) # that pops up to num elements from the stream. Use threads to speed it up. How well does this improve map, filter, and prefixReduce? Why?
