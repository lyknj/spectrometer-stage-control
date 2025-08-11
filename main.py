import seabreeze.spectrometers as sb  ## ocean optics spectrometers
import time
import os  ## interacting w files/directories


from PyQt5 import QtWidgets 


## import classes for linear stages, initialize & connect


from linear_stage_x import LinearStageX
from linear_stage_y import LinearStageY


stage_x = LinearStageX()
stage_y = LinearStageY()


ports_x = stage_x.find_devices()
ports_y = stage_y.find_devices()


stage_x.connect('COM5')  
stage_y.connect('COM6')


## initialize spectrometer 


devices = sb.list_devices()
spec = sb.Spectrometer.from_first_available()
spec.integration_time_micros(100_000) ## set exposure time

## ensure “spectra/” exists, find all existing run folders, calculates next run num. and creates new folder
def get_new_run_directory(base="spectra"):
    os.makedirs(base, exist_ok=True) 

    existing_runs = [d for d in os.listdir(base) if d.startswith("run_") and os.path.isdir(os.path.join(base, d))]

    run_numbers = [int(name.split("_")[1]) for name in existing_runs if name.split("_")[1].isdigit()]
    next_run_number = max(run_numbers, default=0) + 1

    run_dir = os.path.join(base, f"run_{next_run_number}")
    os.makedirs(run_dir)
    return run_dir

## intialize stop button

stop_requested = False

def request_stop():
    global stop_requested
    stop_requested = True

## snake scan 

def scan(stage_x, stage_y, spec,
         x_start = 0, x_end = 28, x_step = 2,
         y_start = 0, y_end = 28, y_step = 2,
         wait_time = 0.1,
         gui = None):
    
    global stop_requested
    stop_requested = False  # reset flag at start of scan

    run_dir = get_new_run_directory() ## create new subfolder
   
    # set list of y positions & moves to next pos
    y_positions = list(range(y_start, y_end + 1, y_step)) 
    for i, y_pos in enumerate(y_positions):

        if stop_requested:
                print("Scan stopped by user.")
                return
        
        stage_y.move(y_pos)
        print(f"Moved Y to {y_pos}")
        time.sleep(wait_time)
        
	# updates GUI with y pos
        if gui is not None:
             gui.y_pos.setText(str(y_pos))
             QtWidgets.QApplication.processEvents()

	# sets list of x positions (alternating directions)
        x_positions = (
            list(range(x_start, x_end + 1, x_step)) if i % 2 == 0
            else list(range(x_end, x_start - 1, -x_step))
        )
	
	# moves x to next pos
        for x_pos in x_positions:

            if stop_requested:
                print("Scan stopped by user.")
                return
            
            stage_x.move(x_pos)
            print(f"Moved X to {x_pos}")
            time.sleep(wait_time)

	# update GUI with x pos
            if gui is not None:
                gui.x_pos.setText(str(x_pos))
                QtWidgets.QApplication.processEvents()
	
		# gets data from spec
            wavelengths = spec.wavelengths()
            intensities = spec.intensities()


		# saves spectrum as a CSV file
            filename = os.path.join(run_dir, f"spectrum_y{y_pos}_x{x_pos}.csv")
            with open(filename, "w") as f:
                f.write("Wavelength,Intensity\n")
                for wl, inten in zip(wavelengths, intensities):
                    f.write(f"{wl},{inten}\n")
            print(f"Saved {filename}")


# single scan 
def move_to_position(stage_x, stage_y, x_target, y_target, wait_time=0.1):
    stage_y.move(y_target)
    print(f"Moved Y to {y_target}")
    time.sleep(wait_time)

    stage_x.move(x_target)
    print(f"Moved X to {x_target}")
    time.sleep(wait_time)











