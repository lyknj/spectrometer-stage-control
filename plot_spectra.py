# plot_spectra.py
# Reads all saved spectrum CSV files from a given run, extracts the intensity at a target wavelength, and visualizes the values as a heatmap using matplotlib.

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set base folder, run folder, and target wavelength for visualization
base_dir = "spectra"
run_name = "run_20250746"
run_path = os.path.join(base_dir, run_name)
target_wavelength = 638  # wavelength (nm) to extract from each spectrum

# Dictionary to store spectra for each (x, y) position
data = {}
for x in range(29):
    for y in range(29):
        # Build the file path for the current spectrum
        filepath = os.path.join(run_path, f"spectrum_y{y}_x{x}.csv")
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)  # load spectrum into DataFrame
            data[(x, y)] = df           # store spectrum with its coordinates

# Matrix to store extracted intensity values for each (y, x) position
intensity_map = np.zeros((29, 29))

# Extract intensity at the closest wavelength to the target for each spectrum
for (x, y), df in data.items():
    idx = (df["Wavelength"] - target_wavelength).abs().idxmin()  # find closest wavelength index
    intensity_map[y, x] = df.loc[idx, "Intensity"]               # assign intensity to matrix

# Plot heatmap (flipped left-right for display purposes)
plt.imshow(np.fliplr(intensity_map), cmap='hot', origin='lower')

plt.title(f"Heatmap at {target_wavelength} nm")
plt.colorbar(label="Intensity")
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.show()
