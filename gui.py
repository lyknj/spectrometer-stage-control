from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
import os
import pandas as pd
import matplotlib.pyplot as plt
import glob

from main import stage_x, stage_y, spec, scan, move_to_position, request_stop

## custom widget class for stage control
class StageWidget(QWidget):

## initialize parent QWidget
    def __init__(self):
        super().__init__()


        loadUi('./test.ui', self) 


        ## connect buttons
        self.home.clicked.connect(self.home_clicked)
        self.go.clicked.connect(self.go_clicked)
        self.stop.clicked.connect(self.stop_clicked)
        self.show.clicked.connect(self.show_clicked)


    def home_clicked(self):
        move_to_position(stage_x, stage_y, 0, 0)
        self.x_pos.setText("0")
        self.y_pos.setText("0")


    def go_clicked(self):
        x_target = int(self.x_target.text())
        y_target = int(self.y_target.text())


        mode = self.mode_selection.currentText()


        if mode == "Single Scan":
            move_to_position(stage_x, stage_y, x_target, y_target)
            self.x_pos.setText(str(x_target))
            self.y_pos.setText(str(y_target))
        else:
            x_step = int(self.x_step.text())
            y_step = int(self.y_step.text())


            scan(stage_x, stage_y, spec,
                 x_start=0, x_end=x_target, x_step=x_step,
                 y_start=0, y_end=y_target, y_step=y_step,
                 gui = self)
           
    def stop_clicked(self):
        print("Stop button clicked")
        request_stop()

    def show_clicked(self):
        x_target = int(self.x_target.text())
        y_target = int(self.y_target.text())


        # Find the most recent run folder
        run_dirs = sorted(glob.glob("spectra/run_*"), key=os.path.getmtime)
        if not run_dirs:
            print("No run folders found.")
            return
        latest_run = run_dirs[-1]


        # Build expected file name
        file_path = os.path.join(latest_run, f"spectrum_y{y_target}_x{x_target}.csv")
        
        if not os.path.exists(file_path):
            print(f"No spectrum found for position ({x_target}, {y_target}).")
            return


        # Load and plot spectrum
        df = pd.read_csv(file_path)
        plt.figure(figsize=(8, 5))
        plt.plot(df["Wavelength"], df["Intensity"], label=f"({x_target}, {y_target})")
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Intensity")
        plt.title(f"Spectrum at position X={x_target}, Y={y_target}")
        plt.legend()
        plt.grid(True)
        plt.show()




from PyQt5.QtWidgets import QMainWindow


## constructor for main window
class StageGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stage Controller")


        # create widget and add it to the window
        self.stage_widget = StageWidget()
        self.setCentralWidget(self.stage_widget)


        self.show()


    def closeEvent(self, *args, **kwargs):
        self.stage_widget.close()
        super(QMainWindow, self).closeEvent(*args, **kwargs)


import sys
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StageGui()
    sys.exit(app.exec_())






