import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


## define folder & file to read + specific wavelength to visualize
base_dir = "spectra"
run_name ="run_20250746"
run_path = os.path.join(base_dir, run_name)
target_wavelength = 638

## load all spectrum files
data = {} ## dict to store spectra
for x in range(29): 
    for y in range(29): 
	## path to current file
        filepath = os.path.join(run_path, f"spectrum_y{y}_x{x}.csv")
        if os.path.exists(filepath): 
            df = pd.read_csv(filepath) ## load into df
            data[(x, y)] = df ## store it into dict


## initialize matrix to store intensity values
intensity_map = np.zeros((29, 29)) 


## loop thru each spectrum
for (x, y), df in data.items():
    idx = (df["Wavelength"] - target_wavelength).abs().idxmin() ## find index of closest wl
    intensity_map[y, x] = df.loc[idx, "Intensity"] ## set intensity value


## shop “hot” heatmap & mirror it
plt.imshow(np.fliplr(intensity_map), cmap='hot', origin='lower')


plt.title(f"Heatmap at {target_wavelength} nm")
plt.colorbar(label="Intensity")
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.show()