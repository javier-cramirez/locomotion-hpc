import numpy as np
import rasterio
import plotly.graph_objects as go

path = "/Users/javierramirez/Desktop/tif_files/RandomMountainIDK.tin.tif"

with rasterio.open(path) as src:
    dem = src.read(1).astype(np.float32)
    nodata = src.nodata
    transform = src.transform  # affine: pixel->map units (usually meters)

if nodata is not None:
    dem = np.where(dem == nodata, np.nan, dem)

# Downsample for interactivity (adjust 400 to taste)
target = 400
step = max(1, max(dem.shape) // target)
Z = dem[::step, ::step]
Z = np.where(np.isnan(Z), np.nanmean(Z), Z)

# Clip outliers so colors aren't dominated
zmin, zmax = np.percentile(Z, [2, 98])
Z = np.clip(Z, zmin, zmax)

# Build X/Y in meters using pixel size from transform
# transform.a = pixel width, transform.e = pixel height (negative sometimes)
px = float(transform.a) * step
py = abs(float(transform.e)) * step

ny, nx = Z.shape
x = np.arange(nx) * px
y = np.arange(ny) * py

fig = go.Figure(data=[go.Surface(x=x, y=y, z=Z, colorscale="earth")])

fig.update_layout(
    title="Interactive DEM (meters)",
    scene=dict(
        xaxis_title="x (m)",
        yaxis_title="y (m)",
        zaxis_title="elevation (m)",
        aspectmode="manual",
        aspectratio=dict(x=1, y=1, z=0.2),  # reduce z exaggeration
    ),
    margin=dict(l=0, r=0, b=0, t=40),
)

fig.show()
#fig.write_html("dem_3d.html", include_plotlyjs="cdn")
#print("Saved dem_3d.html")

