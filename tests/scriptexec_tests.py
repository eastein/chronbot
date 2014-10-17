import unittest
import script_execute as se

class MockedIO(object) :
	def __init__(self) :
		self.log = list()
		self.ihooks = set()

	def on_recv(self, text) :
		self.log.append(('in', text))
		for ih in set(self.ihooks) :
			self.termination_wrap(ih, ih, text)

	def termination_wrap(self, ih, c, *args, **kwargs) :
		try :
			c(*args, **kwargs)
			return True
		except se.Unhook :
			#print 'terminate noted'
			if ih in self.ihooks :
				self.ihooks.remove(ih)
			self.log.append(('terminate', None))
			return False

	def setup_execution(self, initialize_function, ihook) :
		if self.termination_wrap(ihook, initialize_function) :
			self.ihooks.add(ihook)
	
	def send(self, text) :
		#print 'sending %s' % text
		self.log.append(('out', text))

class ScriptTests(unittest.TestCase) :
	def _setup_script(self, scripttext) :
		s = se.Script(scripttext)
		mio = MockedIO()
		e = s.execute(mio.setup_execution, mio.send) # shouldn't maybe MockedIO be a mixin for this sort of thing with a better interface?
		return (s,mio,e)

	def test_onestatement(self) :
		s, mio, e = self._setup_script("hello world")
		self.assertEquals(len(mio.log), 2)
		self.assertEquals(mio.log[0], ("out", "hello world"))
		self.assertEquals(mio.log[1], ("terminate", None))

	def test_read_send(self) :
		s, mio, e = self._setup_script("|!text mike")
		self.assertEquals(len(mio.log), 0)
		mio.on_recv("hi mike")
		self.assertEquals(len(mio.log), 3)
		self.assertEquals(mio.log[0], ("in", "hi mike"))
		self.assertEquals(mio.log[1], ("out", "!text mike hi mike"))
		self.assertEquals(mio.log[2], ("terminate", None))

	def test_read_twice_send(self) :
		s, mio, e = self._setup_script("||!text mike")
		self.assertEquals(len(mio.log), 0)
		mio.on_recv("hi mike")
		mio.on_recv("whats going on")
		self.assertEquals(len(mio.log), 4)
		self.assertEquals(mio.log[0], ("in", "hi mike"))
		self.assertEquals(mio.log[1], ("in", "whats going on"))
		self.assertEquals(mio.log[2], ("out", "!text mike whats going on"))
		self.assertEquals(mio.log[3], ("terminate", None))
