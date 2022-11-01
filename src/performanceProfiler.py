import imgui
import glfw
import array

import circularBuffer

class PerformanceProfiler:
	def __init__(self, window):
		self.window = window
		# Rendering engine
		self.lastFrameTime = 0.0
		self.deltaTime = 0.0
		self.frameTimeSamples = circularBuffer.CircularBuffer(100)
		self.frameTimeAverage = 0.0
		self.frameTimeMin = 0.0
		self.frameTimeMax = 0.0

		# Physics engine
		self.lastTickTime = 0.0
		self.fixedDeltaTime = 0.0
		self.tickTimeSamples = circularBuffer.CircularBuffer(100)
		self.tickTimeAverage = 0.0
		self.tickTimeMin = 0.0
		self.tickTimeMax = 0.0

	def fixedUpdate(self):
		# Compute statistics
		self.fixedDeltaTime = glfw.get_time() - self.lastTickTime
		self.lastTickTime = glfw.get_time()
		self.tickTimeSamples.push(self.fixedDeltaTime)

		self.tickTimeAverage = self.tickTimeSamples.sum() / len(self.tickTimeSamples)
		self.tickTimeMin = self.tickTimeSamples.min()
		self.tickTimeMax = self.tickTimeSamples.max()

	def render(self):
		# Compute statistics
		self.deltaTime = glfw.get_time() - self.lastFrameTime
		self.lastFrameTime = glfw.get_time()
		self.frameTimeSamples.push(self.deltaTime)

		self.frameTimeAverage = self.frameTimeSamples.sum() / len(self.frameTimeSamples)
		self.frameTimeMin = self.frameTimeSamples.min()
		self.frameTimeMax = self.frameTimeSamples.max()

		imgui.begin("Performance Profiler")

		imgui.begin_child("Rendering Engine", 0, 235, True)
		imgui.text("Rendering engine")

		windowSize = glfw.get_window_size(self.window)
		imgui.text("Window size: " + str(windowSize[0]) + "x" + str(windowSize[1]))
		imgui.text("Frame time: " + str(round(self.deltaTime, 4)) + "s")
		imgui.text("Frame time average: " + str(round(self.frameTimeAverage, 4)) + "s")
		imgui.text("Average frames per second: " + str(round(1.0 / self.frameTimeAverage, 3)))
		imgui.text("Frame time min: " + str(round(self.frameTimeMin, 4)) + "s")
		imgui.text("Frame time max: " + str(round(self.frameTimeMax, 4)) + "s")

		# Plot the frame time as a histogram from the last 100 frame times
		histogramValues = array.array('f')
		for i in range(len(self.frameTimeSamples)):
			histogramValues.append(self.frameTimeSamples[i])
		imgui.plot_histogram(
			"",
			histogramValues,
			-1,
			-1,
			None,
			0.0,
			self.frameTimeMax,
			(400, 100)
		)

		imgui.end_child()
		imgui.begin_child("Physics Engine", 0, 115, True)
		imgui.text("Physics engine")

		imgui.text("Fixed delta time: " + str(round(self.fixedDeltaTime, 4)) + "s")
		imgui.text("Fixed delta time average: " + str(round(self.tickTimeAverage, 4)) + "s")
		if self.tickTimeAverage > 0.0:
			imgui.text("Average ticks per second: " + str(round(1.0 / self.tickTimeAverage, 3)))
		else:
			imgui.text("Average ticks per second: inf")
		imgui.text("Fixed delta time min: " + str(round(self.tickTimeMin, 4)) + "s")
		imgui.text("Fixed delta time max: " + str(round(self.tickTimeMax, 4)) + "s")

		imgui.end_child()

		imgui.end()
