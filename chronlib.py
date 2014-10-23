import datetime
import re

class InvalidPatternException(Exception): 
	pass

PT_NUM = re.compile('^([0-9]+)$')
PT_RNG = re.compile('^([0-9]+)\-([0-9]+)$')
PT_DIV = re.compile('^\*/([0-9]+)$')

class CronPattern(object) :
	def __init__(self, pattern, disjunct=True) :
		self.pattern = pattern
		
		self.match_all = False
		self.disjunct = disjunct
		self.checker = None
		
		if self.disjunct and (',' in self.pattern) :
			self.subpatterns = [CronPattern(p, disjunct=False) for p in self.pattern.split(',')]
		else :
			self.disjunct = False

			if self.pattern == '*' :
				self.match_all = True
				return

			m_num = PT_NUM.match(self.pattern)
			m_rng = PT_RNG.match(self.pattern)
			m_div = PT_DIV.match(self.pattern)

			if m_num :
				mv = int(m_num.groups()[0])
				self.checker = lambda v: v == mv
				return
			elif m_rng :
				v1,v2 = m_rng.groups()
				v1,v2 = int(v1), int(v2)
				self.checker = lambda v: (v >= v1) and (v <= v2)
				return
			elif m_div :
				mv = int(m_div.groups()[0])
				self.checker = lambda v: (v % mv) == 0
				return

			raise InvalidPatternException("Unable to parse %s" % self.pattern)

	def check(self, value) :
		if self.match_all :
			return True
		
		if self.disjunct :
			for p in self.subpatterns :
				if p.check(value) :
					return True
			return False

		if self.checker is not None :
			return self.checker(value)
		
		return False

	def __str__(self) :
		return self.pattern

class CronLine(object) :
	def __init__(self, m, h, dom, mon, dow, command=None) :
		self.m = CronPattern(m)
		self.h = CronPattern(h)
		self.dom = CronPattern(dom)
		self.mon = CronPattern(mon)
		self.dow = CronPattern(dow)
		self.command = command

	def match(self, dt) :
		if not self.m.check(dt.minute) :
			return False
		if not self.h.check(dt.hour) :
			return False
		if not self.dom.check(dt.day) : # TODO how does modulus work?
			return False
		if not self.mon.check(dt.month) : # TODO handle names, how does modulus work?
			return False
		if not self.dow.check((dt.weekday() + 1) % 7) : # TODO handle names
			return False
		return True

	def __str__(self) :
		r = ' '.join([str(self.m),str(self.h), str(self.dom), str(self.mon), str(self.dow)])
		if self.command is not None :
			r += ' ' + str(self.command)
		return r
