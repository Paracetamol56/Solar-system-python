
class CircularBuffer:
	def __init__(self, size):
		self.size = size
		self.buffer = [None for i in range(size)]
		self.head = 0
		self.tail = 0

	def push(self, item):
		self.buffer[self.head] = item
		self.head = (self.head + 1) % self.size
		if self.head == self.tail:
			self.tail = (self.tail + 1) % self.size

	def pop(self):
		item = self.buffer[self.tail]
		self.tail = (self.tail + 1) % self.size
		return item
	
	def __len__(self):
		return (self.head - self.tail) % self.size
	
	def __getitem__(self, index):
		return self.buffer[(self.tail + index) % self.__len__()]

	def resize(self, size):
		self.size = size
		self.buffer = [None for i in range(size)]
		self.head = 0
		self.tail = 0