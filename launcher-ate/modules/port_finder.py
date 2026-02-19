# launcher-ate/modules/port_finder.py
import serial.tools.list_ports
from modules.util import get_base_dir, logger, write_exception_to_log


"""2 Port Info: apply_usb_info=<bound method ListPortInfo.apply_usb_info of <serial.tools.list_ports_common.ListPortInfo object at 0x000001FD640E1D90>>, description=USB Serial Device (COM5), device=COM5, hwid=USB VID:PID=2E8A:000A SER=E6631417A32A9330, interface=None, location=None, manufacturer=Microsoft, name=COM5, pid=10, product=None, serial_number=E6631417A32A9330, usb_description=COM5, usb_info=USB VID:PID=2E8A:000A SER=E6631417A32A9330, vid=11914"""
"""3 Port Info: apply_usb_info=<bound method ListPortInfo.apply_usb_info of <serial.tools.list_ports_common.ListPortInfo object at 0x000001FD641167A0>>, description=USB Serial Device (COM6), device=COM6, hwid=USB VID:PID=239A:80F4 SER=E6614C311B637C37, interface=None, location=None, manufacturer=Microsoft, name=COM6, pid=33012, product=None, serial_number=E6614C311B637C37, usb_description=COM6, usb_info=USB VID:PID=239A:80F4 SER=E6614C311B637C37, vid=9114"""

class Port_finder:
    """Finds available ports for the application"""
    
    def __init__(self):
        self.base_dir = get_base_dir()
        self.serial_ports = []

    def get_port(self):
        ports = self.get_serial_ports

        
    def get_serial_ports(self):
        self.serial_ports.clear()
        self.serial_ports =serial.tools.list_ports.comports()
        return self.serial_ports
    
    def find_port_candidates(self):
        candidates = filter(lambda port: port.hwid.lower().find("usb") != -1, self.get_serial_ports())
        candidates = filter(lambda port: port.description.lower().find("serial") != -1, candidates)
        tmp = filter(lambda port: port.vid in [11914, 9114] , candidates)
        if tmp: 
            return list(tmp)
        return list(candidates)
    def select_port(self):
        try:
            return self.find_port_candidates()[0]
        except IndexError:
            return None



    

