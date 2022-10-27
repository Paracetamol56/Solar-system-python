import imgui
from imgui.integrations.glfw import GlfwRenderer
import glfw
import OpenGL.GL as gl
import math

import date

from constants import _KM_PER_PIXEL
from constants import _KM_PER_AU

class System:
	def __init__(self, name, objects = []):
		self.name = name
		self.objects = objects
		self.date = date.Date()
		self.timeScale = 1.0
		self.systemScale = 1.0
		self.radiusScale = 1.0
		self.radiusNormalization = 0.0
		self.showGrid = False
		self.gridColor = [0.1, 0.1, 0.1, 1.0]

		self.meanRadius = 0.0

		for key in self.objects:
			self.meanRadius += key.radius
		self.meanRadius /= self.objects.__len__()

	def validate(self):
		for i in range(len(self.objects)):
			for j in range(i + 1, len(self.objects)):
				if self.objects[i].name == self.objects[j].name:
					return False
	
	def render(self):
		# Update date and time based on time scale
		self.date.increment(self.timeScale / 10000)

		imgui.set_cursor_pos([0, 0])
		drawList = imgui.get_background_draw_list()
		
		windowSize = glfw.get_window_size(glfw.get_current_context())

		if self.showGrid:
			gridStep = int((_KM_PER_AU / _KM_PER_PIXEL) * self.systemScale)
			color = imgui.get_color_u32_rgba(
				self.gridColor[0],
				self.gridColor[1],
				self.gridColor[2],
				self.gridColor[3]
			)
			# Horizontal lines
			# Bottom half
			for i in range (0, windowSize[1] // 2, gridStep):
				drawList.add_line(0, windowSize[1] // 2 + i, windowSize[0], windowSize[1] // 2 + i, color)
			# Top half
			for i in range (0, windowSize[1] // 2, gridStep):
				drawList.add_line(0, windowSize[1] // 2 - i, windowSize[0], windowSize[1] // 2 - i, color)
			# Vertical lines
			# Left half
			for i in range (0, windowSize[0] // 2, gridStep):
				drawList.add_line(windowSize[0] // 2 - i, 0, windowSize[0] // 2 - i, windowSize[1], color)
			# Right half
			for i in range (0, windowSize[0] // 2, gridStep):
				drawList.add_line(windowSize[0] // 2 + i, 0, windowSize[0] // 2 + i, windowSize[1], color)

		# Draw objects
		if self.objects.__len__() < 1:
			return
		
		# The first object is the center of the system and should be drawn first
		self.objects[0].render(drawList, windowSize, self.systemScale, self.radiusScale, self.radiusNormalization, self.meanRadius)

		# Draw other objects
		for i in range(1, self.objects.__len__()):
			self.objects[i].orbit.update(self.date)
			self.objects[i].render(drawList, windowSize, self.systemScale, self.radiusScale, self.radiusNormalization, self.meanRadius)


class Planet:
	def __init__(self, name, radius, mass, color, orbit):
		self.name = name
		self.visible = True
		self.radius = radius
		self.mass = mass
		self.color = color
		self.orbit = orbit
	
	def render(self, drawList, windowSize, systemScale, radiusScale, radiusNormalization, meanRadius):
		if not self.visible:
			return

		systemScale /= _KM_PER_PIXEL

		# Compute radius
		# Normalize radius
		radius = self.radius * (1 - radiusNormalization) + meanRadius * radiusNormalization
		# Scale radius
		radius *= radiusScale / _KM_PER_PIXEL

		# Draw planet
		drawList.add_circle_filled(
			windowSize[0] / 2 + self.orbit.x * systemScale,
			windowSize[1] / 2 + self.orbit.y * systemScale,
			radius,
			imgui.get_color_u32_rgba(
				self.color[0],
				self.color[1],
				self.color[2],
				1.0)
			)

class Orbit:
	def __init__(self, semiMajorAxis, periapsis, apoapsis, period, velocity, eccentricity):
		self.semiMajorAxis = semiMajorAxis
		self.periapsis = periapsis
		self.apoapsis = apoapsis
		self.period = period
		self.velocity = velocity
		self.eccentricity = eccentricity

		self.x = 0.0
		self.y = 0.0

	def update(self, date):
		# Calculate position
		currentAngle = (date.getTotalDays() / self.period) % 2 * math.pi
		self.x = self.semiMajorAxis * math.cos(currentAngle)
		self.y = self.semiMajorAxis * math.sin(currentAngle)