import datetime
import unittest
import chronlib as cl

class PatternTests(unittest.TestCase) :
	def test_wildcard(self) :
		p = cl.CronPattern("*")
		self.assertEquals(p.check(0), True)
		self.assertEquals(p.check(7), True)
		self.assertEquals(p.check(28), True)

	def test_num(self) :
		p = cl.CronPattern("3")
		self.assertEquals(p.check(0), False)
		self.assertEquals(p.check(6), False)
		self.assertEquals(p.check(3), True)

	def test_several_nums(self) :
		p = cl.CronPattern("3,6")
		self.assertEquals(p.check(0), False)
		self.assertEquals(p.check(6), True)
		self.assertEquals(p.check(3), True)
		self.assertEquals(p.check(1), False)

	def test_div(self) :
		p = cl.CronPattern("*/5")
		self.assertEquals(p.check(6), False)
		self.assertEquals(p.check(5), True)
		self.assertEquals(p.check(10), True)
		self.assertEquals(p.check(3), False)

	def test_badpattern(self) :
		got_err = False
		try :
			p = cl.CronPattern('7,uhhhh,*/5,40-50')
		except cl.InvalidPatternException, ipe :
			self.assertEquals(ipe.message, "Unable to parse uhhhh")
			got_err = True

		self.assertTrue(got_err)

class LineTests(unittest.TestCase) :
	def test_dailymidnight(self) :
		l = cl.CronLine("0", "0", "*", "*", "*")
		self.assertTrue(l.match(datetime.datetime(2014, 10, 19, 0, 0, 0)))
		self.assertFalse(l.match(datetime.datetime(2014, 10, 18, 23, 59, 0)))
		self.assertFalse(l.match(datetime.datetime(2014, 10, 19, 1, 0, 0)))
		self.assertFalse(l.match(datetime.datetime(2014, 10, 19, 0, 1, 0)))

	def test_stringify(self) :
		self.assertEquals(str(cl.CronLine("0", "0", "*", "*", "*", 'hi')), "0 0 * * * hi")

	def test_equality(self) :
		a = cl.CronLine("0", "0", "*", "*", "*", 'hi')
		_a = cl.CronLine("0", "0", "*", "*", "*", 'hi')
		b = cl.CronLine("0", "1", "*", "*", "*", 'hi')
		self.assertEquals(a, _a)
		self.assertNotEquals(a, b)
		self.assertNotEquals(a, None)

	def test_to_dict(self) :
		a = cl.CronLine("0", "1", "2", "3", "*", 'hello world')
		self.assertEquals({
			'm': '0',
			'h': '1',
			'dom': '2',
			'mon': '3',
			'dow': '*',
			'command': 'hello world'
		}, a.to_dict())

	def test_from_dict(self) :
		a = cl.CronLine("0", "1", "2", "3", "*", 'hello world')
		self.assertEquals(cl.CronLine.from_dict({
			'm': '0',
			'h': '1',
			'dom': '2',
			'mon': '3',
			'dow': '*',
			'command': 'hello world'
		}), a)
