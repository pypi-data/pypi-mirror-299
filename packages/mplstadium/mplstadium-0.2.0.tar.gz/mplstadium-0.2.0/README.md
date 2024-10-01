**A Python plotting library to visualize stadium data**

![Lint and Test](https://github.com/Peter4137/mplstadium/actions/workflows/action.yml/badge.svg)

# Quick start

Install the package using `pip` (or `pip3`).

```
pip install mplstadium
```

Plot an outdoor 400m running track, with the origin at the centre of the track:


```python
from mplstadium.utils import OutdoorAthleticsTrack2D
from matplotlib import pyplot as plt

track = OutdoorAthleticsTrack2D()
fig, ax = track.draw()
ax.set_aspect("equal")
plt.show()
```

<p align="center">
    <img src="https://github.com/Peter4137/mplstadium/blob/main/figs/outdoor_athletics_track.png?raw=true">
</p>

Plot an Olympic Velodrome in 3D and a trajectory on the surface:

```python
from mplstadium.utils import OlympicVelodrome3D
import numpy as np
from matplotlib import pyplot as plt

track = OlympicVelodrome3D()
fig, ax = track.draw()

s = np.linspace(0, 250, 250)
d = 4 + 4 * np.sin(s / 10)

track.trajectory(s, d, c="r")

ax.set_aspect("equal")
ax.axis("off")
plt.show()
```

<p align="center">
  <img src="https://github.com/Peter4137/mplstadium/blob/main/figs/olympic_velodrome_3d_trajectory.png?raw=true" width="75%">
</p>

Define a custom Stadium geometry and plot scatter points over it:

```python
from mplstadium import Stadium3D
import numpy as np
from matplotlib import pyplot as plt

stadium_length = 20 + 2 * np.pi * 10

track = Stadium3D(
    length=stadium_length,
    radius=10,
    width=20,
    straight_banking=30,
    curve_banking=30,
    lane_widths=[20],
    surface_color="black",
    infield_color="green",
)
fig, ax = track.draw()

s = np.random.uniform(0, stadium_length, 200)
d = np.random.uniform(0, 20, 200)

track.scatter(s, d, c="r", alpha=1)

ax.set_aspect("equal")
ax.axis("off")
plt.show()
```

<p align="center">
  <img src="https://github.com/Peter4137/mplstadium/blob/main/figs/custom_stadium_scatter.png?raw=true" width="75%">
</p>

# Development

To run the test suite:
```
poetry run pytest --mpl
```

To regenerate the baseline images for the plot tests:
```
poetry run pytest --mpl-generate-path=baseline
```

# License

[MIT](https://raw.githubusercontent.com/mlsedigital/mplbasketball/main/LICENSE.txt)