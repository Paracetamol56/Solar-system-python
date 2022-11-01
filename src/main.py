import imgui
from imgui.integrations.glfw import GlfwRenderer
import glfw
import OpenGL.GL as gl
import json

import configWindow
import performanceProfiler
import system
import celestialBody

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
configWindow = configWindow.ConfigWindow()
performanceProfiler = performanceProfiler.PerformanceProfiler(window)
stellarSystem = system.System()
filePath = "data/solarSystem.json"
# filePath = "data/binaryStars.json"
# filePath = "data/tatooSystem.json"

# Initialise the system from the json file
objects = json.load(open(filePath, "r"))
for key in objects:
	newBody = celestialBody.CelestialBody2D(
		key["name"],
		key["radius"],
		key["mass"],
		key["color"],
		key["velocity"],
		key["position"],
	)
	stellarSystem.addBody(newBody)

# Main loop
while not glfw.window_should_close(window):
	glfw.poll_events()
	impl.process_inputs()

	# Call solarSystem.fixedUpdate() at a fixed rate
	if glfw.get_time() - lastPhysicTick > 1 / physicTickPerSecond:
		stellarSystem.fixedUpdate()
		performanceProfiler.fixedUpdate()
		lastPhysicTick = glfw.get_time()

	imgui.new_frame()

	configWindow.render(stellarSystem)
	performanceProfiler.render()
	stellarSystem.render()

	# Clear the glfw window
	glfw.make_context_current(window)
	gl.glClearColor(
		configWindow.backgroundColor[0],
		configWindow.backgroundColor[1],
		configWindow.backgroundColor[2],
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
