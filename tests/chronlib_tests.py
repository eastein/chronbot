import unittest
import chronlib as cl

class ChronlibTests(unittest.TestCase) :
	def test_wildcard(self) :
		p = cl.CronPattern("*")
		self.assertEquals(p.check(0), True)
		self.assertEquals(p.check(7), True)
		self.assertEquals(p.check(28), True)
