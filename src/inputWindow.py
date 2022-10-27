import imgui
from imgui.integrations.glfw import GlfwRenderer
import glfw
import OpenGL.GL as gl
import datetime

import date

class InputWindow:
	def __init__(self):
		self.dateCollapseVisible = True
		self.dateCollapseVisible = True
		self.objectCollapseVisible = True
		self.animationCollapseVisible = True
		self.renderingCollapseVisible = True
		self.backgroundColor = [0, 0, 0]
	
	def render(self, system):
		# ImGui window for configuration
		imgui.begin("Configuration")

		# Collapsing header for date
		expanded, self.dateCollapseVisible = imgui.collapsing_header("Date", True)
		if expanded:
			todayButton = imgui.button("Today")
			if todayButton:
				currentTime = datetime.datetime.now()
				system.date = date.Date()

			# Date input
			_, system.date.day = imgui.input_int("Day", system.date.day)
			_, system.date.month = imgui.input_int("Month", system.date.month)
			_, system.date.year = imgui.input_int("Year", system.date.year)

			# Date validation
			system.date.purge()

		# Collapsing header for time
		expanded, dateCollapseVisible = imgui.collapsing_header("Time", True)
		if expanded:
			nowButton = imgui.button("Now")
			if nowButton:
				currentTime = datetime.datetime.now()
				system.date = date.Date()

			# Time input
			_, system.date.hour = imgui.input_int("Hour", system.date.hour)
			_, system.date.minute = imgui.input_int("Minute", system.date.minute)
			_, system.date.second = imgui.input_int("Second", system.date.second)

			# Time validation
			system.date.purge()
		
		# Collapsing header for objects
		expanded, self.objectCollapseVisible = imgui.collapsing_header("System", True)
		if expanded:
			# Objects checkbox
			for key in system.objects:
				_, key.visible = imgui.checkbox(key.name, key.visible)
				if key.visible:
					# Customisation button
					imgui.same_line()
					imgui.spacing()
					imgui.same_line()
					imgui.button(">", 20, 20)
					if imgui.is_item_clicked():
							imgui.open_popup(key.name)

					# Popup for customisation
					if imgui.begin_popup(key.name):
						imgui.text("Customising " + key.name)
						_, key.radius = imgui.input_float("Radius (km)", key.radius)
						_, key.color = imgui.color_edit3(
							"Color",
							key.color[0],
							key.color[1],
							key.color[2],
						)
						imgui.end_popup()

		# Collapsing header for animation
		expanded, self.animationCollapseVisible = imgui.collapsing_header("Animation", True)
		if expanded:
			# Time scale input
			_, system.timeScale = imgui.drag_float("Time scale", system.timeScale, 1, 0.0, 1000.0)

		# Collapsing header for rendering
		expanded, self.renderingCollapseVisible = imgui.collapsing_header("Rendering", True)
		if expanded:
			# System scale input
			_, system.systemScale = imgui.drag_float("System scale", system.systemScale, 0.01, 0.01, 10.0)

			# Radius scale input
			_, system.radiusScale = imgui.drag_float("Radius scale", system.radiusScale, 0.1, 0.01, 100.0)

			# Radius normalization input
			_, system.radiusNormalization = imgui.drag_float("Radius normalization", system.radiusNormalization, 0.01, 0.0, 1.0)
			if imgui.is_item_hovered():
				imgui.set_tooltip("0.0 = no normalization, scales are respected\n1.0 = maximum normalization, all objects have the same size")

			# Background color input
			_, self.backgroundColor = imgui.color_edit3(
				"Background color",
				self.backgroundColor[0],
				self.backgroundColor[1],
				self.backgroundColor[2],
			)

			# Show grig checkbox
			_, system.showGrid = imgui.checkbox("Show grid", system.showGrid)
			if imgui.is_item_hovered():
				imgui.set_tooltip("One unit is equal to 1 astronomical unit")

			# Grid color input
			_, system.gridColor = imgui.color_edit4(
				"Grid color",
				system.gridColor[0],
				system.gridColor[1],
				system.gridColor[2],
				system.gridColor[3],
			)

			# Trails checkbox
			_, system.showTrails = imgui.checkbox("Trails", system.showTrails)

			# Trails length input
			_, system.trailLength = imgui.drag_int("Trails length", system.trailLength, 1, 5, 100)

			# Trails color input
			_, system.trailColor = imgui.color_edit4(
				"Trails color",
				system.trailColor[0],
				system.trailColor[1],
				system.trailColor[2],
				system.trailColor[3],
			)

		imgui.end()