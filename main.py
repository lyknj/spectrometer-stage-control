# Coordinates scanning between the X/Y linear stages and spectrometer

import seabreeze.spectrometers as sb  # Ocean Optics spectrometers
import time
import os
from PyQt5 import QtWidgets


# Import our stage classes
from linear_stage_x import LinearStageX
from linear_stage_y import LinearStageY


# Initialize stage objects
x_stage = LinearStageX()
y_stage = LinearStageY()


# Find and connect to stages
ports_x = x_stage.find_devices()
ports_y = y_stage.find_devices()


x_stage.connect('COM5')  # Replace with your X-axis COM port
y_stage.connect('COM6')  # Replace with your Y-axis COM port


# Initialize spectrometer
devices = sb.list_devices()
spectrometer = sb.Spectrometer.from_first_available()
spectrometer.integration_time_micros(100_000)  # Exposure time in microseconds

# Creates a new folder for each scan, incrementing run numbers
def get_new_run_directory(base="spectra"):
    os.makedirs(base, exist_ok=True)
    existing_runs = [d for d in os.listdir(base) if d.startswith("run_") and os.path.isdir(os.path.join(base, d))]
    run_numbers = [int(name.split("_")[1]) for name in existing_runs if name.split("_")[1].isdigit()]
    next_run_number = max(run_numbers, default=0) + 1
    run_dir = os.path.join(base, f"run_{next_run_number}")
    os.makedirs(run_dir)
    return run_dir

# Initialize stop button

stop_requested = False

def request_stop():
    global stop_requested
    stop_requested = True


# Snake Scan - Moves the Y stage in steps, scanning X in opposite directions each row
def scan(x_stage, y_stage, spectrometer,
        x_start=0, x_end=28, x_step=2,
        y_start=0, y_end=28, y_step=2,
        wait_time=0.1, gui=None):


    global stop_requested
    stop_requested = False


    run_dir = get_new_run_directory()


    y_positions = list(range(y_start, y_end + 1, y_step))
    for i, y_pos in enumerate(y_positions):
        if stop_requested:
            print("Scan stopped by user.")
            return


        y_stage.move(y_pos)
        print(f"Moved Y to {y_pos}")
        time.sleep(wait_time)


        if gui is not None:
            gui.y_pos.setText(str(y_pos))
            QtWidgets.QApplication.processEvents()


           # Alternate X direction each row
        x_positions = list(range(x_start, x_end + 1, x_step)) if i % 2 == 0 else list(range(x_end, x_start - 1, -x_step))


        for x_pos in x_positions:
            if stop_requested:
                print("Scan stopped by user.")
                return


            x_stage.move(x_pos)
            print(f"Moved X to {x_pos}")
            time.sleep(wait_time)


            if gui is not None:
                gui.x_pos.setText(str(x_pos))
                QtWidgets.QApplication.processEvents()


               # Capture spectrum
            wavelengths = spectrometer.wavelengths()
            intensities = spectrometer.intensities()


               # Save to CSV
            filename = os.path.join(run_dir, f"spectrum_y{y_pos}_x{x_pos}.csv")
            with open(filename, "w") as f:
                f.write("Wavelength,Intensity\n")
                for wl, inten in zip(wavelengths, intensities):
                    f.write(f"{wl},{inten}\n")
            print(f"Saved {filename}")

            