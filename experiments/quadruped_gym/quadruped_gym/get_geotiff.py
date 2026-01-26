import numpy as np
import rasterio
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa

path = "/mnt/c/Users/jrsts/Downloads/output.tin/output.tin.tif"

with rasterio.open(path) as src:
    dem = src.read(1).astype(np.float32)
    nodata = src.nodata

if nodata is not None:
    dem = np.where(dem == nodata, np.nan, dem)

# Downsample for speed (DEM can be huge)
step = max(1, dem.shape[0] // 300)  # aim ~300x300
Z = dem[::step, ::step]

# Fill NaNs for plotting
Z = np.where(np.isnan(Z), np.nanmean(Z), Z)

# Build X/Y grid in "pixels"
ny, nx = Z.shape
X, Y = np.meshgrid(np.arange(nx), np.arange(ny))

# Robust z-limits (avoid outliers making it look crazy)
zmin, zmax = np.percentile(Z, [2, 98])

fig = plt.figure(figsize=(11, 8))
ax = fig.add_subplot(111, projection="3d")

ax.plot_surface(X, Y, Z, cmap="terrain", linewidth=0, antialiased=True, rstride=1, cstride=1)

ax.set_title("DEM 3D Surface (downsampled)")
ax.set_xlabel("x (pixels)")
ax.set_ylabel("y (pixels)")
ax.set_zlabel("elevation (m)")
ax.set_zlim(zmin, zmax)

# Make it not look vertically exaggerated
try:
    ax.set_box_aspect((1, 1, 0.25))
except Exception:
    pass

plt.savefig("dem_3d.png", dpi=200, bbox_inches="tight")
plt.close()
print("Saved dem_3d.png")


