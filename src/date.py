import datetime
import math
from unicodedata import decimal

class Date:
	def __init__(self):
		currentTime = datetime.datetime.now()
		
		self.day = currentTime.day
		self.month = currentTime.month
		self.year = currentTime.year
		self.hour = currentTime.hour
		self.minute = currentTime.minute
		self.second = currentTime.second

	def __str__(self):
		return str(self.day) + "/" + str(self.month) + "/" + str(self.year) + " " + str(self.hour) + ":" + str(self.minute) + ":" + str(self.second)

	def purge(self):
		# Clamp month to 1-12
		if self.month < 1:
				self.month = 1
		elif self.month > 12:
				self.month = 12

		# Clamp day depending on month and leap year
		if self.day < 1:
				self.day = 1
		if self.month == 2:
				if self.year % 4 == 0:
						if self.day > 29:
								self.day = 29
				else:
						if self.day > 28:
								self.day = 28
		elif self.month in [4, 6, 9, 11]:
				if self.day > 30:
						self.day = 30
		else:
				if self.day > 31:
						self.day = 31

		# Clamp hour to 0-23
		if self.hour < 0:
				self.hour = 0
		elif self.hour > 23:
				self.hour = 23

		# Clamp minute to 0-59
		if self.minute < 0:
				self.minute = 0
		elif self.minute > 59:
				self.minute = 59

		# Clamp second to 0-59
		if self.second < 0:
				self.second = 0
		elif self.second > 59:
				self.second = 59
	
	def getTotalDays(self):
		totalDays = self.year * 365.25

		for month in range(1, self.month):
			if month == 2:
				if self.year % 4 == 0:
					totalDays += 29
				else:
					totalDays += 28
			elif month in [4, 6, 9, 11]:
				totalDays += 30
			else:
				totalDays += 31

		totalDays += self.day

		totalDays += self.hour / 24
		totalDays += self.minute / 1440
		totalDays += self.second / 86400

		return totalDays

	def increment(self, day):
		if day <= 0:
			return

		# Precomppute the number of days in the current month
		daysInMonth = 0
		if self.month == 2:
			if self.year % 4 == 0:
				daysInMonth = 29
			else:
				daysInMonth = 28
		elif self.month in [4, 6, 9, 11]:
			daysInMonth = 30
		else:
			daysInMonth = 31

		# Increment the day
		if self.day + math.ceil(day) > daysInMonth:
			# Hard case
			self.day = 1
			if self.month == 12:
				self.month = 1
				self.year += 1
			else:
				self.month += 1
		else:
			# Easy case
			self.day += math.floor(day)

		# Increment the hour
		hour = (day - math.floor(day)) * 24
		if self.hour + math.ceil(hour) > 23:
			# Hard case
			self.hour = 0
			self.increment(1)
		else:
			# Easy case
			self.hour += math.floor(hour)
		
		# Increment the minute
		minute = (hour - math.floor(hour)) * 60
		if self.minute + math.ceil(minute) > 59:
			# Hard case
			self.minute = 0
			self.increment(1)
		else:
			# Easy case
			self.minute += math.floor(minute)

		# Increment the second
		second = (minute - math.floor(minute)) * 60
		if self.second + math.ceil(second) > 59:
			# Hard case
			self.second = 0
			self.increment(1)
		else:
			# Easy case
			self.second += math.floor(second)
			
		self.purge()