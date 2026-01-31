import numpy as np
import rasterio
import matplotlib.pyplot as plt

from scipy.ndimage import zoom, gaussian_filter  # pip install scipy
import imageio.v2 as imageio                     # pip install imageio

in_tif = "/Users/javierramirez/Desktop/tif_files/NorthMountain1.tin.tif"
out_png = "terrain_hfield_16bit.png"

# ---- settings you control ----
target_n = 257              # 257, 513, 1025 are good MuJoCo sizes
smooth_sigma = 1.0          # 0 = no smoothing; 1–3 is common for walkable terrain
z_scale_m = 5.0             # max height range in meters in MuJoCo (pick 1–20 depending on area)
xy_half_extent_m = 50.0     # half-width/half-length in meters => terrain is 100m x 100m
# ------------------------------

with rasterio.open(in_tif) as src:
    elev = src.read(1).astype(np.float32)
    nodata = src.nodata
    transform = src.transform
    crs = src.crs

print("CRS:", crs)
print("Transform:", transform)
print("Raw min/max:", float(np.nanmin(elev)), float(np.nanmax(elev)), "nodata:", nodata)

# 1) Mask nodata (your -9999)
if nodata is None:
    # common fallback: treat very negative values as nodata
    nodata = -9999.0
mask = (elev == nodata) | ~np.isfinite(elev)
elev = np.where(mask, np.nan, elev)

# If everything is nan, stop
if np.isnan(elev).all():
    raise ValueError("All DEM values are NaN after nodata masking. Check your nodata value/path.")

# 2) Fill NaNs (simple but effective)
# Fill with median of valid pixels
fill_val = np.nanmedian(elev)
elev = np.where(np.isnan(elev), fill_val, elev)

print("After nodata fill min/max:", float(elev.min()), float(elev.max()))

# 3) Crop to a square (center crop) then resample to target_n x target_n
h, w = elev.shape
side = min(h, w)
r0 = (h - side) // 2
c0 = (w - side) // 2
elev_sq = elev[r0:r0+side, c0:c0+side]

scale = target_n / side
elev_rs = zoom(elev_sq, zoom=scale, order=1)  # bilinear

# 4) Optional smoothing (reduces tiny spikes)
if smooth_sigma and smooth_sigma > 0:
    elev_rs = gaussian_filter(elev_rs, sigma=smooth_sigma)

# 5) Normalize to [0,1] for MuJoCo heightfield image
elev_rs -= elev_rs.min()
rng = elev_rs.max() - elev_rs.min()
if rng < 1e-8:
    raise ValueError("Terrain has near-zero height range after processing.")
elev_norm = elev_rs / rng

# 6) Save as 16-bit PNG
img16 = (elev_norm * 65535).astype(np.uint16)
imageio.imwrite(out_png, img16)
print(f"Saved: {out_png} (16-bit PNG)")

# 7) Save debug previews
#plt.figure(figsize=(7,6))
#plt.imshow(elev_norm, cmap="terrain")
#plt.colorbar(label="normalized height [0,1]")
#plt.title("Heightfield (normalized)")
#plt.axis("off")
#plt.savefig("terrain_preview.png", dpi=200, bbox_inches="tight")
#plt.close()
#print("Saved: terrain_preview.png")

# 8) Tell you what to put in MuJoCo XML
print("\nMuJoCo XML snippet:")
print(f'''<asset>
  <hfield name="terrain" file="{out_png}" size="{xy_half_extent_m} {xy_half_extent_m} {z_scale_m} 0.1"/>
</asset>

<worldbody>
  <geom type="hfield" hfield="terrain" pos="0 0 0" rgba="0.6 0.5 0.4 1"/>
</worldbody>''')

print("\nNotes:")
print("- size = x_half y_half z_scale base_thickness")
print("- Your PNG is [0,1]; z_scale_m sets max elevation variation in meters.")
