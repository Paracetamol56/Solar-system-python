import imgui
from imgui.integrations.glfw import GlfwRenderer
import OpenGL.GL as gl

class InputWindow:
	def __init__(self):
		self.objectCollapseVisible = True
		self.animationCollapseVisible = True
		self.renderingCollapseVisible = True
		self.backgroundColor = [0, 0, 0]
	
	def render(self, system):
		# ImGui window for configuration
		imgui.begin("Configuration")

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
					imgui.button("Style")
					if imgui.is_item_clicked():
						imgui.open_popup("Style-" + key.name)
					imgui.same_line()
					imgui.button("Physics")
					if imgui.is_item_clicked():
						imgui.open_popup("Physics-" + key.name)

					# Popup for customisation
					if imgui.begin_popup("Style-" + key.name):
						imgui.text("Customising " + key.name + " style")
						_, key.radius = imgui.drag_float("Radius (m)", key.radius)
						_, key.color = imgui.color_edit3(
							"Color",
							key.color[0],
							key.color[1],
							key.color[2],
						)
						imgui.end_popup()

					# Popup for physics
					if imgui.begin_popup("Physics-" + key.name):
						imgui.text("Customising " + key.name + " physics")
						_, key.mass = imgui.input_float("Mass (kg)", key.mass)
						_, key.position[0] = imgui.input_float("X position (m)", key.position[0])
						_, key.position[1] = imgui.input_float("Y position (m)", key.position[1])
						_, key.velocity[0] = imgui.input_float("X velocity (m/s)", key.velocity[0])
						_, key.velocity[1] = imgui.input_float("Y velocity (m/s)", key.velocity[1])
						_, key.acceleration[0] = imgui.input_float("X acceleration (m/s²)", key.acceleration[0])
						_, key.acceleration[1] = imgui.input_float("Y acceleration (m/s²)", key.acceleration[1])
						imgui.end_popup()

		# Collapsing header for animation
		expanded, self.animationCollapseVisible = imgui.collapsing_header("Animation", True)
		if expanded:
			# Time scale input
			_, system.timeScale = imgui.drag_float("Time scale", system.timeScale, 1, 0.0, 100.0)

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

		imgui.end()