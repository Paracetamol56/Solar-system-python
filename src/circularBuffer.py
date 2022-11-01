
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
		return self.buffer[(self.tail + index) % self.size]

	def sum(self):
		sum = 0
		for i in range(len(self)):
			sum += self[i]
		return sum

	def min(self):
		min = self[0]
		for i in range(len(self)):
			if self[i] < min:
				min = self[i]
		return min
	
	def max(self):
		max = self[0]
		for i in range(len(self)):
			if self[i] > max:
				max = self[i]
		return max

	def resize(self, size):
		self.size = size
		self.buffer = [None for i in range(size)]
		self.head = 0
		self.tail = 0