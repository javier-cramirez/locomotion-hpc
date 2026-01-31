import matplotlib
matplotlib.use("Agg")   # force headless backend

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from opensimplex import OpenSimplex

def generate_fractal_opensimplex(
    n=257, scale=150.0, octaves=3, persistence=0.25, lacunarity=3.0, seed=0
):
    noise = OpenSimplex(seed)
    terrain = np.zeros((n, n))

    amp = 0.8
    freq = 1.0 / scale

    for _ in range(octaves):
        for i in range(n):
            for j in range(n):
                terrain[i, j] += amp * noise.noise2(i * freq, j * freq)
        amp *= persistence
        freq *= lacunarity

    terrain -= terrain.min()
    terrain /= terrain.max() + 1e-8

    max_height = 0.0001
    terrain = terrain * max_height
    return terrain


terrain = generate_fractal_opensimplex()

# Create grid
x = np.linspace(0, 1, terrain.shape[0])
y = np.linspace(0, 1, terrain.shape[1])
X, Y = np.meshgrid(x, y)

# Plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")

ax.plot_surface(
    X, Y, terrain,
    cmap="terrain",
    linewidth=0,
    antialiased=True,
    rstride=2,
    cstride=2
)

ax.set_title("OpenSimplex Terrain (3D)")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("height")

plt.savefig("terrain_3d1.png", dpi=100, bbox_inches="tight")
plt.close()

print("Saved terrain_3d.png")

