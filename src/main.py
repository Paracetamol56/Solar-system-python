import imgui
from imgui.integrations.glfw import GlfwRenderer
import glfw
import OpenGL.GL as gl

import date
import inputWindow
import system

# Setup window with glfw
glfw.init()
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
glfw.window_hint(glfw.RESIZABLE, True)
window = glfw.create_window(1280, 720, "Solar system", None, None)
glfw.make_context_current(window)

# Setup ImGui binding
imgui.create_context()
impl = GlfwRenderer(window)

# Global variables
inputWindow = inputWindow.InputWindow()
solarSystem = system.System("solar system", [
	system.Planet("Sun", 695700, 1, [0.949, 0.407, 0.145, 1], system.Orbit(0, 0, 0, 1, 0, 0)),
	system.Planet("Mercury", 2439, 1, [0.494, 0.498, 0.498, 1], system.Orbit(57909100, 46000000, 69800000, 87.97, 47.87, 0.20564)),
	system.Planet("Venus", 6051, 1, [0.686, 0.576, 0.435, 1], system.Orbit(108209000, 107477000, 108940000, 224.7, 35.02, 0.0068)),
	system.Planet("Earth", 6371, 1, [0.129, 0.176, 0.376, 1], system.Orbit(149598023, 147095000, 152100000, 365.26, 29.78, 0.0167)),
	system.Planet("Mars", 3389, 1, [0.713, 0.227, 0, 1], system.Orbit(227943824, 206700000, 249200000, 686.98, 24.13, 0.0934)),
	system.Planet("Jupiter", 69911, 1, [0.698, 0.682, 0.517, 1], system.Orbit(778340821, 740520000, 816000000, 4332.59, 13.07, 0.0489)),
	system.Planet("Saturn", 58232, 1, [0.866, 0.772, 0.576, 1], system.Orbit(1426666422, 1352550000, 1500750000, 10759.22, 9.69, 0.0565)),
	system.Planet("Uranus", 25362, 1, [0.666, 0.800, 0.823, 1], system.Orbit(2870658186, 2743000000, 3000000000, 30685.4, 6.81, 0.046381)),
	system.Planet("Neptune", 24622, 1, [0.196, 0.309, 0.890, 1], system.Orbit(4498396441, 4444000000, 4553000000, 60189, 5.43, 0.009456)),
	# RIP Pluto
])

# #b73a00 to rgb = 0.713, 0.227, 0

# Main loop
while not glfw.window_should_close(window):
	glfw.poll_events()
	impl.process_inputs()

	imgui.new_frame()

	inputWindow.render(solarSystem)
	solarSystem.render()

	# Clear the glfw window
	glfw.make_context_current(window)
	gl.glClearColor(
		inputWindow.backgroundColor[0],
		inputWindow.backgroundColor[1],
		inputWindow.backgroundColor[2],
		1
	)
	gl.glClear(gl.GL_COLOR_BUFFER_BIT)

	# Rendering
	imgui.render()
	impl.render(imgui.get_draw_data())

	glfw.swap_buffers(window)

# Shutdown
impl.shutdown()
imgui.destroy_context()
glfw.terminate()
