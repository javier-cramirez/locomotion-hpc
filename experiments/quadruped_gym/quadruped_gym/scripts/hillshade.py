import numpy as np
import rasterio
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def hillshade(dem, azimuth=315, altitude=45):
    # compute gradients
    dy, dx = np.gradient(dem)
    slope = np.pi/2 - np.arctan(np.sqrt(dx*dx + dy*dy))
    aspect = np.arctan2(-dx, dy)

    az = np.deg2rad(azimuth)
    alt = np.deg2rad(altitude)

    shaded = (np.sin(alt) * np.sin(slope) +
              np.cos(alt) * np.cos(slope) * np.cos(az - aspect))
    return (shaded - shaded.min()) / (shaded.max() - shaded.min() + 1e-8)

path = "/mnt/c/Users/jrsts/Downloads/output.tin/output.tin.tif"

with rasterio.open(path) as src:
    dem = src.read(1).astype(np.float32)
    nodata = src.nodata
if nodata is not None:
    dem = np.where(dem == nodata, np.nan, dem)

# fill NaNs for shading (simple fill)
m = np.nanmean(dem)
dem_filled = np.where(np.isnan(dem), m, dem)

hs = hillshade(dem_filled)

plt.figure(figsize=(8, 7))
plt.imshow(hs, cmap="gray")
plt.title("Hillshade")
plt.axis("off")
plt.savefig("hillshade.png", dpi=200, bbox_inches="tight")
plt.close()

print("Saved hillshade.png")

