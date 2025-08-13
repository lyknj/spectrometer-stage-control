# Handles communication with the X-axis Thorlabs ELL17 linear stage

import elliptec
import sys, os

class LinearStageX():
    # Automatically initializes variables when the object is created

   def __init__(self):
       self.ports = None        # List of available COM ports
       self.device = None       # The connected stage device object
       self._controller = None  # Controller object for sending commands


   def find_devices(self):
       # Scan the computer for connected ELL17 controllers
       ports = elliptec.scan.find_ports()
       self.ports = ports[:]    # Store ports in object variable
       return ports

   def connect(self, idn):
       # Create a controller for the given COM port
       self._controller = elliptec.Controller(idn, debug=True)
       self._controller.port = idn

       # Find devices connected to the controller
       self.devices = elliptec.scan_for_devices(controller=self._controller)

       # Create a Linear stage object for control
       self.device = elliptec.Linear(self._controller)
       return self.device.info  # Return device information

   def move(self, pos):
       # Move the stage to a specific position (mm)
       sys.stdout = open(os.devnull, 'w')  # Suppress stage output
       position = self.device.set_distance(pos)
       sys.stdout = sys.__stdout__
       return position
   
   