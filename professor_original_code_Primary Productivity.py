import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# -------------------------------
# Step 1: File paths
# -------------------------------
chl_path = r"D:/SUST/OCG Lecturer/Remote sensing/2025/Value_Added_Product/AQUA_MODIS.20030101_20250131.L3m.MC.CHL.chlor_a.4km.nc"
sst_path = r"D:/SUST/OCG Lecturer/Remote sensing/2025/Value_Added_Product/AQUA_MODIS.20030101_20250131.L3m.MC.NSST.sst.4km.nc"
par_path = r"D:/SUST/OCG Lecturer/Remote sensing/2025/Value_Added_Product/AQUA_MODIS.20030101_20250131.L3m.MC.PAR.par.4km.nc"

# -------------------------------
# Step 2: Load datasets
# -------------------------------
chl_ds = xr.open_dataset(chl_path)
sst_ds = xr.open_dataset(sst_path)
par_ds = xr.open_dataset(par_path)

# -------------------------------
# Step 3: Subset Bay of Bengal region
# Latitude: 5N–25N, Longitude: 80E–100E
# -------------------------------
chl = chl_ds['chlor_a'].sel(lat=slice(25, 5), lon=slice(80, 100))
sst = sst_ds['sst'].sel(lat=slice(25, 5), lon=slice(80, 100))
par = par_ds['par'].sel(lat=slice(25, 5), lon=slice(80, 100))

# -------------------------------
# Step 4: Mask invalid values
# -------------------------------
chl = chl.where((chl > 0) & (chl < 20))
sst = sst.where((sst > -2) & (sst < 45))
par = par.where((par > 0) & (par < 100))

# -------------------------------
# Step 5: Compute PBopt from SST (empirical fit)
# -------------------------------
pb_opt = 1.2956 + 0.2749 * sst - 0.03285 * sst**2 + 0.001033 * sst**3

# -------------------------------
# Step 6: Estimate Euphotic Depth (Ze)
# -------------------------------
ze = 38 * chl**-0.428  # Morel (1988) formula

# -------------------------------
# Step 7: Compute Primary Productivity (VGPM)
# -------------------------------
pp = 0.66125 * pb_opt * chl * ze * (par / (par + 4.1))  # Units: mg C m⁻² day⁻¹

# -------------------------------
# Step 8: Prepare and Plot Output
# -------------------------------
pp_plot = pp.squeeze()  # Remove singleton dimensions

plt.figure(figsize=(10, 8))
pp_plot.plot(cmap='turbo')
plt.title("Estimated Primary Productivity\nBay of Bengal (mg C m⁻² day⁻¹)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig("primary_productivity_bay_of_bengal.png", dpi=300)
plt.show()

# -------------------------------
# Step 9: Export to CSV
# -------------------------------
df = pp_plot.to_dataframe(name='PrimaryProductivity').reset_index()
df.to_csv("primary_productivity_bay_of_bengal.csv", index=False)
print("Exported results to CSV and PNG successfully.")
