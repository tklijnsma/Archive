try:	# str.rsplit >= Python 2.4
	rsplit = str.rsplit
except:
	def rsplit(x, sep, maxsplit = None):
		""" Split from the right side
		>>> rsplit('abc', '.', 1)
		['abc']
		>>> rsplit('a.b.c.d.e.f.g', '.', 1)
		['a.b.c.d.e.f', 'g']
		>>> rsplit('a.b.c.d.e.f.g', '.', 2)
		['a.b.c.d.e', 'f', 'g']
		"""
		tmp = x.split(sep)
		if len(tmp) > 1:
			return [str.join(sep, tmp[:len(tmp)-maxsplit])] + tmp[len(tmp)-maxsplit:]
		return tmp

try:	# set >= Python 2.4
	set = set
except:
	import sets
	set = sets.Set

try:	# sorted >= Python 2.4
	sorted = sorted
except:
	def sorted(unsortedList, comp = None, key = None):
		""" Sort list by either using the standard comparison method cmp()
		or, if supplied, the function comp.  The optional argument key
		is a function that returns the key to sort by - default is the
		identity function.

		>>> sorted([4, 3, 1, 5, 2])
		[1, 2, 3, 4, 5]

		>>> sorted([4, 3, 1, 5, 2], comp=lambda a, b: -cmp(a, b))
		[5, 4, 3, 2, 1]

		>>> sorted(['spam', 'ham', 'cheese'], key=len)
		['ham', 'spam', 'cheese']

		>>> sorted(['spam', 'ham', 'cheese'], comp=lambda a, b: -cmp(a, b), key=len)
		['cheese', 'spam', 'ham']
		"""

		tmp = list(unsortedList)
		tmp_cmp = comp

		if key and comp:
			tmp_cmp = lambda x, y: comp(key(x), key(y))
		elif key:
			tmp_cmp = lambda x, y: cmp(key(x), key(y))

		if tmp_cmp != None:
			tmp.sort(tmp_cmp)
		else:
			tmp.sort()
		return tmp

try:	# hashlib >= Python 2.5
	import hashlib
	md5 = hashlib.md5
except:
	import md5
	md5 = md5.md5

try:	# next >= Python 2.6
	next = next
except:
	def next(it, *default):
		try:
			return it.next()
		except:
			if default:
				return default[0]
			raise

try:	# raw_input < Python 3.0
	user_input = raw_input
except:
	user_input = input

try:	# any >= Python 2.5
	any = any
except:
	def any(iterable):
		for element in iterable:
			if element:
				return True
		return False

try:	# functools.lru_cache >= Python 3.2
	import functools
	lru_cache = functools.lru_cache
except:
	def lru_cache(fun, maxsize = 10): # Implementation causes CPU performance hit to avoid I/O
		def funProxy(*args, **kargs):
			idx = None
			for (i, value) in enumerate(funProxy.cache):
				if value[0] == (args, kargs):
					idx = i
			if idx != None:
				(key, item) = funProxy.cache.pop(idx)
			else:
				item = funProxy.fun(*args, **kargs)
			funProxy.cache.insert(0, ((args, kargs), item))
			while len(funProxy.cache) > maxsize:
				funProxy.cache.pop()
			return item
		(funProxy.fun, funProxy.cache) = (fun, [])
		return funProxy

if __name__ == '__main__':
	import doctest
	doctest.testmod()

__all__ = ['rsplit', 'set', 'sorted', 'md5', 'next', 'user_input', 'any', 'lru_cache']
