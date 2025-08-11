import elliptec
import sys, os

class LinearStageY():
    ## runs automatically (initializes avail ports, stage device, controller obj)

    def __init__(self):
        self.ports = None
        self.device = None
        self._controller = None

    def find_devices(self):
        ## find where ELLs are plugged in
        ports = elliptec.scan.find_ports() ## searches all ports on comp
        self.ports = ports[:]    ## copies list to "self.ports"
        return ports

    def connect(self, idn):
        self._controller = elliptec.Controller(idn, debug=True)  ## controller should talk to hardware on this "idn" usb port - disables output?
        self._controller.port = idn     ## confirm that the controller knows which port to use
        self.devices = elliptec.scan_for_devices(controller=self._controller) ## returns list of devices connected controller 
        self.device = elliptec.Linear(self._controller) ## create linear device object (linear stage) so commands can be used w it
        return self.device.info ## details on connected stage

    def move(self, pos):
        sys.stdout = open(os.devnull, 'w') ## cleanup so nothing in terminal
        position = self.device.set_distance(pos) 
        sys.stdout = sys.__stdout__ ## undoes line 38
        return position 
    
