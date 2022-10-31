import imgui
from imgui.integrations.glfw import GlfwRenderer
import glfw
import math

import constants
import circularBuffer

class System:
	def __init__(self, objects = []):
		self.objects = objects
		self.timeScale = 1.0
		self.systemScale = 1.0
		self.radiusScale = 1.0
		self.radiusNormalization = 0.0
		self.showTrails = True
		self.trailsLength = 100
		self.trailsColor = [1.0, 1.0, 1.0, 1.0]
		self.trailsResolution = 4
		self.trailsStep = 0
		self.showGrid = False
		self.gridColor = [0.1, 0.1, 0.1, 1.0]
		self.showVelocityVectors = False
		self.velocityVectorLength = 100000
		self.velocityVectorColor = [1.0, 0.0, 0.0, 1.0]
		self.showAccelerationVectors = False
		self.accelerationVectorLength = 100000000
		self.accelerationVectorColor = [0.0, 1.0, 0.0, 1.0]

		self.meanRadius = 0.0

		if self.objects.__len__() > 0:
			for key in self.objects:
				self.meanRadius += key.radius
			self.meanRadius /= self.objects.__len__()

		self.validate()

	def validate(self):
		for i in range(len(self.objects)):
			for j in range(i + 1, len(self.objects)):
				if self.objects[i].name == self.objects[j].name:
					print("Error: Duplicate object name: " + self.objects[i].name)
					exit(1)
	
	def addBody(self, body):
		self.objects.append(body)

		# Update mean radius
		self.meanRadius = 0.0
		for key in self.objects:
			self.meanRadius += key.radius
		self.meanRadius /= self.objects.__len__()

		self.validate()
	
	def fixedUpdate(self):
		for key in self.objects:
			# Reset acceleration
			key.acceleration = [0.0, 0.0]
			
			# Compute object acceleration
			for other in self.objects:
				if other == key:
					continue
				# Compute vector from key to other
				towardVector = [
					other.position[0] - key.position[0],
					other.position[1] - key.position[1]
				]
				# Compute distance (in m)
				distance = math.sqrt(towardVector[0] ** 2 + towardVector[1] ** 2)
				# Compute acceleration thanks to Newton's law of universal gravitation (in m/s^2)
				acceleration = [
					constants._G * other.mass * towardVector[0] / distance ** 3,
					constants._G * other.mass * towardVector[1] / distance ** 3
				]
				# Add acceleration to key
				key.acceleration[0] += acceleration[0] * 1000
				key.acceleration[1] += acceleration[1] * 1000
			# Compute object velocity
			key.velocity[0] += key.acceleration[0] * self.timeScale
			key.velocity[1] += key.acceleration[1] * self.timeScale

			# Update object position
			key.position[0] += key.velocity[0] * self.timeScale * 1000
			key.position[1] += key.velocity[1] * self.timeScale * 1000

			# Pushthe new position to the trail buffer
			if self.showTrails:
				if self.trailsStep >= self.trailsResolution:
					key.trail.push([key.position[0], key.position[1]])
					self.trailsStep = 0
				else:
					self.trailsStep += 1

	def render(self):
		imgui.set_cursor_pos([0, 0])
		drawList = imgui.get_background_draw_list()
		
		windowSize = glfw.get_window_size(glfw.get_current_context())

		if self.showGrid:
			gridStep = int((constants._M_PER_AU / constants._M_PER_PIXEL) * self.systemScale)
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
		
		for key in self.objects:
			if self.showTrails:
				key.renderTrails(drawList, windowSize, self.systemScale, self.trailsColor, self.trailsLength)
			if self.showVelocityVectors:
				key.renderVelocityVector(drawList, windowSize, self.systemScale, self.velocityVectorLength, self.velocityVectorColor)
			if self.showAccelerationVectors:
				key.renderAccelerationVector(drawList, windowSize, self.systemScale, self.accelerationVectorLength, self.accelerationVectorColor)
			key.render(drawList, windowSize, self.systemScale, self.radiusScale, self.radiusNormalization, self.meanRadius)

class CelestialBody2D:
	"""
	Constructor parameters:
		name: Name of the object
		radius: Radius of the object (in m)
		mass: Mass of the object (in kg)
		color: Color of the object
		velocity: Velocity of the object (in m/s)
		initialPosition: Position of the object relative to the center of the system (in m)
	"""
	def __init__(self, name, radius, mass, color, velocity, position):
		self.name = name
		self.visible = True
		self.color = color
		self.radius = radius
		self.mass = mass
		self.velocity = velocity
		self.position = position
		self.acceleration = [0.0, 0.0]
		self.trail = circularBuffer.CircularBuffer(100)
	
	def renderTrails(self, drawList, windowSize, systemScale, trailsColor, trailsLength):
		if self.trail.__len__() < 2:
			return
		if trailsLength != self.trail.size:
			self.trail.resize(trailsLength)
		
		systemScale /= constants._M_PER_PIXEL

		color = imgui.get_color_u32_rgba(
			trailsColor[0],
			trailsColor[1],
			trailsColor[2],
			trailsColor[3]
		)

		for i in range(0, self.trail.__len__() -2):
			if self.trail[i] == None or self.trail[i + 1] == None:
				continue
			drawList.add_line(
				windowSize[0] // 2 + self.trail[i][0] * systemScale,
				windowSize[1] // 2 + self.trail[i][1] * systemScale,
				windowSize[0] // 2 + self.trail[i + 1][0] * systemScale,
				windowSize[1] // 2 + self.trail[i + 1][1] * systemScale,
				color
			)

	def renderVelocityVector(self, drawList, windowSize, systemScale, vectorLength, vectorColor):
		if not self.visible:
			return

		systemScale /= constants._M_PER_PIXEL
		# Draw velocity vector
		color = imgui.get_color_u32_rgba(
			vectorColor[0],
			vectorColor[1],
			vectorColor[2],
			vectorColor[3]
		)
		drawList.add_line(
			# Body position
			windowSize[0] / 2 + self.position[0] * systemScale,
			windowSize[1] / 2 + self.position[1] * systemScale,
			# Body position + velocity vector * vectorLength
			windowSize[0] / 2 + (self.position[0] + self.velocity[0] * vectorLength) * systemScale,
			windowSize[1] / 2 + (self.position[1] + self.velocity[1] * vectorLength) * systemScale,
			color
		)

	def renderAccelerationVector(self, drawList, windowSize, systemScale, vectorLength, vectorColor):
		if not self.visible:
			return
		
		systemScale /= constants._M_PER_PIXEL
		# Draw acceleration vector
		color = imgui.get_color_u32_rgba(
			vectorColor[0],
			vectorColor[1],
			vectorColor[2],
			vectorColor[3]
		)
		drawList.add_line(
			# Body position
			windowSize[0] / 2 + self.position[0] * systemScale,
			windowSize[1] / 2 + self.position[1] * systemScale,
			# Body position + acceleration vector * vectorLength
			windowSize[0] / 2 + (self.position[0] + self.acceleration[0] * vectorLength) * systemScale,
			windowSize[1] / 2 + (self.position[1] + self.acceleration[1] * vectorLength) * systemScale,
			color
		)

	def render(self, drawList, windowSize, systemScale, radiusScale, radiusNormalization, meanRadius):
		if not self.visible:
			return

		systemScale /= constants._M_PER_PIXEL

		# Compute radius
		# Normalize radius
		radius = self.radius * (1 - radiusNormalization) + meanRadius * radiusNormalization
		# Scale radius
		radius *= radiusScale / constants._M_PER_PIXEL

		# Draw planet
		drawList.add_circle_filled(
			windowSize[0] / 2 + self.position[0] * systemScale,
			windowSize[1] / 2 + self.position[1] * systemScale,
			radius,
			imgui.get_color_u32_rgba(
				self.color[0],
				self.color[1],
				self.color[2],
				1.0
			)
		)