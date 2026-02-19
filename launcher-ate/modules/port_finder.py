# launcher-ate/modules/port_finder.py
import serial.tools.list_ports
from serial.tools.list_ports_common import ListPortInfo
from modules.util import get_base_dir, logger, write_exception_to_log
from dataclasses import dataclass


"""2 Port Info: apply_usb_info=<bound method ListPortInfo.apply_usb_info of <serial.tools.list_ports_common.ListPortInfo object at 0x000001FD640E1D90>>, description=USB Serial Device (COM5), device=COM5, hwid=USB VID:PID=2E8A:000A SER=E6631417A32A9330, interface=None, location=None, manufacturer=Microsoft, name=COM5, pid=10, product=None, serial_number=E6631417A32A9330, usb_description=COM5, usb_info=USB VID:PID=2E8A:000A SER=E6631417A32A9330, vid=11914"""
"""3 Port Info: apply_usb_info=<bound method ListPortInfo.apply_usb_info of <serial.tools.list_ports_common.ListPortInfo object at 0x000001FD641167A0>>, description=USB Serial Device (COM6), device=COM6, hwid=USB VID:PID=239A:80F4 SER=E6614C311B637C37, interface=None, location=None, manufacturer=Microsoft, name=COM6, pid=33012, product=None, serial_number=E6614C311B637C37, usb_description=COM6, usb_info=USB VID:PID=239A:80F4 SER=E6614C311B637C37, vid=9114"""

@dataclass
class PortInfo:
    port: ListPortInfo
    # is_serial: bool = False
    is_usb: bool = False
    known_vid: bool = False
    probed: bool = False

class PortFinder:
    """Finds available ports for the application"""

    start_message = "SpearUAV Viper300 launcher test ver"
    
    def __init__(self):
        self.base_dir = get_base_dir()
        self.serial_ports = []
        self.probed_map = {}
        self.inf_current_port = None

        
    def get_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if not hasattr(port, 'description'):
                print(list(filter( lambda k: k.find("__") == -1, dir(port))))
        port_info = map(lambda port: PortInfo(
                        port,
                        # is_serial=port.description.lower().find("serial") != -1,
                        is_usb=port.hwid.lower().find("usb") != -1 ,
                        known_vid=port.vid in [11914, 9114],
                        probed=port_info in self.probed_map)
                        , ports)
        self.serial_ports = list(port_info)
        return self.serial_ports
    
    def probe(self, port:PortInfo):
        #raise NotImplemented("Port_finder.probe")
        try:
            port.port.connect()
            if port.port.read().find(self.start_message) == 0:
                port.probed = True
                self.probed_map[port.port.serial_number] = True
                return True
        except Exception as e:
            return e
        finally:
            try:
                port.port.close()
            except:
                pass
        return False

    
    def find_port_candidates(self):
        candidates = filter(lambda port: port.is_usb, self.get_serial_ports())
        # candidates = filter(lambda port: port.is_serial, candidates)
        candidates = list(candidates)
        tmp = list(filter(lambda port: port.known_vid , candidates))
        if len(tmp): 
            return tmp
        return candidates
    def select_port(self):
        try:
            self.inf_current_port = self.find_port_candidates()[0]
        except IndexError:
            self.inf_current_port = None
        return self.inf_current_port



    

