import datetime

class CronPattern(object) :
	def __init__(self, pattern, disjunct=True) :
		self.pattern = pattern

		self.match_all = False
		self.disjunct = disjunct

		if self.disjunct and (',' in self.pattern) :
			# TODO split and then set up the OR setup
			self.subpatterns = [CronPattern(p) for p in self.pattern.split(',')]
		else :
			self.disjunct = False

			if self.pattern == '*' :
				self.match_all = True
			else :
				pass



	def check(self, value) :
		if self.disjunct :
			# TODO do the or bit
			return False
		
		if self.match_all :
			return True

		return False

class CronLine(object) :
	def __init__(self, m, h, dom, mon, dow, command) :
		self.m = CronPattern(m)
		self.h = CronPattern(h)
		self.dom = CronPattern(dom)
		self.mon = CronPattern(mon)
		self.dow = CronPattern(dow)
		self.command = command
