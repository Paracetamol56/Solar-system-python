# Solar system simulation

![overview](doc/overview.png)

## Overview

### Context

This is a homework assignment with the theme of "Solar system". The language have to be Python and the dataset is freely chosen.
I chose to make a physics simulation of the solar system with real data.

### Tech stack

This is a solar system simulation written in Python and using the PyImGUI library for the GUI (Python bindings for the C++ library Dear ImGUI), the PyOpenGL library for the OpenGL bindings and the GLFW library for the window management.

## Usage

### Requirements

- Python 3

### Installation

- Clone the repository with the following command :

```bash
git clone https://github.com/Paracetamol56/Solar-system-python.git
cd Solar-system-python
```

- Install the dependencies with the following command :

```bash
pip install -r requirements.txt
```

### Run

- Run the simulation with the following command :

```bash
python src/main.py
```

### Configuration

Once the application is running, you can configure the simulation with the following panel :

![configuration](doc/config-panel.png)

- **System** : Under this section, you can check/uncheck the bodies you want to render, customize the color of each body and change their radius individually. You also have access to read-only physical informations about each body (mass, position, velocity, acceleration). As always, units are following the international system of units (SI). The coordinates origin is the center the screen.

- **Animation** : Here, you can change the `Time scale` paramter which is used to speed up or slow down the simulation.

- **Rendering** : First, you can change the `System scale` parameter which is used to zoom in or out the system. Then, you can change the `Radius scale` parameter which is used to scale the radius of each body. Note that this parameter is independent from the `System scale` parameter.<br>
The `Radius normalization` is a convienient parameter added to be able to see very small bodies along with very big ones. At 0, the radius scale is perfectly respected. At 1, the radius scale is ignored and all bodies are rendered with the same radius.<br>
Additionally, you can change the `Background color` to your liking.<br>
Finaly, you can enable or disable the grid and change its color. The grid size is fixed to 1 astronomical unit (AU), which is the average distance between the Earth and the Sun.
<br><br>
NB: By default, the scale parameters are set to 1.0, so the system is rendered at its natural size, with respected radius and distances.

## Data

**IMPORTANT :** Every number used in the simulation is in the metric system (meters, kilograms, seconds, etc.).

For the solar system reproduction, I gathered data from the [NASA website](https://nssdc.gsfc.nasa.gov/planetary/factsheet/) for each planet and the sun.
Data concerning celestial bodies are stored in the `data/` folder as JSON files (on file per system).

You are free create a brand new stellar system with hipotetical data, but you have to respect the JSON format.
