class Unhook(Exception) :
	pass

class ScriptExecution(object) :
	def __init__(self, script_object, initialize_register_hook, output_hook) :
		self.script_object = script_object
		self.operations = list(self.script_object.operations)
		self.operation_idx = 0
		self.operation_count = len(self.operations)
		self.input_buffer = None

		self.l_output = output_hook
		initialize_register_hook(self.step, self.l_input)


	# TODO make this actually execute. Operations that are null strings should just set the script engine to wait for a line. Operations that aren't null strings should send the line and then wait for a line.

	def termination_check(self) :
		if self.operation_idx >= self.operation_count :
			raise Unhook

	def l_input(self, text) :
		self.step('input', text)

	def step(self, mode='tick', text=None) :
		running = True
		while running :
			self.termination_check()
			operation = self.operations[self.operation_idx]
			if operation == '' :
				# this means read plain input, but we won't be doing that unless there actually is input to read
				if mode == 'input' : 
					# buffer the input
					self.input_buffer = text
					# let the rloop run the next ocmmand
					self.operation_idx += 1
					mode = 'tick' 
				else :
					running = False
			else :
				if self.input_buffer is not None :
					operation = '%s %s' % (operation, self.input_buffer)
					self.input_buffer = None # used buffer up

				# send xarg'd command
				self.l_output(operation)

				# TODO transform this command into an input command & don't bump the index, if theres nothing after this.
				if self.operation_idx == self.operation_count - 1 :
					self.operation_idx += 1
				else :
					self.operations[self.operation_idx] = ''

				running = False
		self.termination_check()

class Script(object) :
	def __init__(self, code_text) :
		self.code_text = code_text
		self.operations = self.code_text.split('|')

	def execute(self, initialize_register_hook, output_hook) :
		"""
		@param input_register_hook is a callable that takes one parameter - another callable. Calling input_register_hook(c) should cause input events to be executed on c with c(line_of_text).
		@parma output_hook is a callable that will send outputs if called with a line of text.
		"""
		return ScriptExecution(self, initialize_register_hook, output_hook)
