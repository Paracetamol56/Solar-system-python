import imgui
from imgui.integrations.glfw import GlfwRenderer
import glfw
import OpenGL.GL as gl

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
physicTickPerSecond = 30
lastPhysicTick = glfw.get_time()
inputWindow = inputWindow.InputWindow()
solarSystem = system.System([
	system.CelestialBody2D("Sun", 6.957e8, 1.989e30, [0.949, 0.407, 0.145, 1], [0.0, 0.0], [0.0, 0.0]),
	system.CelestialBody2D("Earth", 6.3781e6, 5.972e24, [0.0, 0.0, 1.0, 1], [0.0, -2.978e4], [1.4959787e11, 0.0]),
	# RIP Pluto
])

# Main loop
while not glfw.window_should_close(window):
	glfw.poll_events()
	impl.process_inputs()

	# Call solarSystem.fixedUpdate() at a fixed rate
	if glfw.get_time() - lastPhysicTick > 1 / physicTickPerSecond:
		solarSystem.fixedUpdate()
		lastPhysicTick = glfw.get_time()

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
glfw.terminate()
