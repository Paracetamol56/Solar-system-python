import imgui

import constants
import circularBuffer

class CelestialBody2D:
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