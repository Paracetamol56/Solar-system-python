import imgui
import glfw
import math

import constants
class System:
	def __init__(self, objects = []):
		self.objects = objects
		self.timeScale = 1.0
		self.systemScale = 1.0
		self.radiusScale = 1.0
		self.radiusNormalization = 0.0
		self.showTrails = True
		self.trailsLength = 100
		self.trailsColor = [0.039, 0.262, 0.509, 0.51]
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

		for key in self.objects:
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
