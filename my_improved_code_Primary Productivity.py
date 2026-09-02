import os
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

# Step 1: File paths 
folder_path = r"C:\Users\Lenovo\Downloads\Portfolio Projects\Primary Productivity"

chl_name = "AQUA_MODIS.20260101_20260131.L3m.MO.CHL.chlor_a.4km.nc"
sst_name = "AQUA_MODIS.20260101_20260131.L3m.MO.NSST.sst.4km.nc"
par_name = "AQUA_MODIS.20260101_20260131.L3m.MO.PAR.par.4km.nc"

chl_path = os.path.join(folder_path, chl_name)
sst_path = os.path.join(folder_path, sst_name)
par_path = os.path.join(folder_path, par_name)

print("🔄 Loading NetCDF datasets using netcdf4 engine...")

# Step 2: Load datasets
chl_ds = xr.open_dataset(chl_path, engine="netcdf4")
sst_ds = xr.open_dataset(sst_path, engine="netcdf4")
par_ds = xr.open_dataset(par_path, engine="netcdf4")

# Step 3: Subset Bay of Bengal region
# Latitude: 5N–25N, Longitude: 80E–100E

chl = chl_ds['chlor_a'].sel(lat=slice(25, 5), lon=slice(80, 100))
sst = sst_ds['sst'].sel(lat=slice(25, 5), lon=slice(80, 100))
par = par_ds['par'].sel(lat=slice(25, 5), lon=slice(80, 100))

# Step 4: Mask invalid values
chl = chl.where((chl > 0) & (chl < 20))
sst = sst.where((sst > -2) & (sst < 45))
par = par.where((par > 0) & (par < 100))

# Step 5: Compute PBopt from SST (empirical fit)
pb_opt = 1.2956 + 0.2749 * sst - 0.03285 * sst**2 + 0.001033 * sst**3

# Step 6: Estimate Euphotic Depth (Ze)
# Safety Check: Guard against exact zero values causing math domain crashes
chl_safe = np.clip(chl, 0.001, None)
ze = 38 * chl_safe**-0.428  # Morel (1988) formula

# Step 7: Compute Primary Productivity (VGPM)
pp = 0.66125 * pb_opt * chl * ze * (par / (par + 4.1))  # Units: mg C m⁻² day⁻¹

# Step 8: Prepare and Plot Output
pp_plot = pp.squeeze()  # Remove singleton dimensions

fig, ax = plt.subplots(figsize=(11, 8))

# Map plot configurations using native axes to bypass cartopy dependencies
lon_vals = pp_plot['lon'].values
lat_vals = pp_plot['lat'].values
pp_vals = pp_plot.values

# Render the primary productivity data grid
img = ax.pcolormesh(lon_vals, lat_vals, pp_vals, cmap='turbo', shading='auto')

# Aesthetic Grid & Extent adjustments
ax.set_xlim(80, 100)
ax.set_ylim(5, 25)
ax.set_xticks(np.arange(80, 101, 4))
ax.set_yticks(np.arange(5, 26, 4))
ax.set_xticklabels([f"{x}°E" for x in np.arange(80, 101, 4)], fontsize=10)
ax.set_yticklabels([f"{y}°N" for y in np.arange(5, 26, 4)], fontsize=10)
ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.4)

# Set the background to light gray so missing values over land show up as a solid map background
ax.set_facecolor('lightgray')

# Formatting labels
ax.set_title("MODIS-Based Primary Productivity Estimation Using the VGPM – Bay of Bengal", fontsize=13, pad=15)
ax.set_xlabel("Longitude", fontsize=11, labelpad=8)
ax.set_ylabel("Latitude", fontsize=11, labelpad=8)

# Colorbar adjustments
cbar = plt.colorbar(img, orientation='vertical', pad=0.03, aspect=30, shrink=1)
cbar.set_label("Primary Productivity (mg C m⁻² day⁻¹)", fontsize=11, labelpad=10)

plt.tight_layout()

# Save image 
png_out = os.path.join(folder_path, "primary_productivity_bay_of_bengal.png")
plt.savefig(png_out, dpi=300)
plt.show()

# Step 9: Export to CSV (Saved cleanly to same folder path)
print("csv Exporting results to CSV dataset...")
df = pp_plot.to_dataframe(name='PrimaryProductivity').reset_index()
csv_out = os.path.join(folder_path, "primary_productivity_bay_of_bengal.csv")
df.to_csv(csv_out, index=False)

print(f"\n🚀 Success! Outputs saved securely to your portfolio folder:\n -> Graph: {png_out}\n -> Data: {csv_out}")
