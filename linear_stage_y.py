# Handles communication with the Y-axis Thorlabs ELL17 linear stage
# Almost identical to LinearStageX

import elliptec
import sys, os


class LinearStageY():
    def __init__(self):
        self.ports = None
        self.device = None
        self._controller = None


    def find_devices(self):
        ports = elliptec.scan.find_ports()
        self.ports = ports[:]
        return ports


    def connect(self, idn):
        self._controller = elliptec.Controller(idn, debug=True)
        self._controller.port = idn
        self.devices = elliptec.scan_for_devices(controller=self._controller)
        self.device = elliptec.Linear(self._controller)
        return self.device.info

    def move(self, pos):
        sys.stdout = open(os.devnull, 'w')
        position = self.device.set_distance(pos)
        sys.stdout = sys.__stdout__
        return position