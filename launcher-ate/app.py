

from colorama import Fore, Back, Style, just_fix_windows_console
from pathlib import Path
from enum import IntEnum,auto
from modules.logo_reader import LogoReader
from modules.test_reader import TestReader
from modules.port_finder import PortFinder
import traceback
from modules.util import  set_base_dir, get_base_dir, logger, setup_logger,\
    write_exception_to_log, clear_terminal
from menu.style import PALETTE as P
from menu.main_menu import render_main_menu

# Initialize BASE_DIR directly
set_base_dir(__file__)

class App():
    """Main app, orchestrates and runs stuff"""

    NO_TEST_INFO = "No tests Found"
    NOT_AVAILABLE = "NA"

    def __init__(self):
        self.logo_reader = LogoReader(get_base_dir())
        self.logo:str = None
        self.tests = TestReader()
        self.testinfo = self.NO_TEST_INFO
        self.port_finder = PortFinder()
        self.port = None
        self.operator_name = self.NOT_AVAILABLE
        self.launcher_sn = self.NOT_AVAILABLE
        self.test_start_time = self.NOT_AVAILABLE
        self.load_exception_happend = False
        self.state = None
        
    
    def run(self):
        clear_terminal()
        self.load_data()
        self.state = self.main_menu
        while True:
            try:
                self.state()
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:                
                write_exception_to_log()
    
    def load_data(self):
        try:
            self.logo = self.logo_reader.read()
            print(self.logo)
            print(Style.RESET_ALL)
        except Exception as e:
            self.load_exception_happend = True
            write_exception_to_log()
            self.logo = f"\t{Fore.YELLOW} Logo warning: {Style.RESET_ALL}{e}"
            print(self.logo)
        try:
            self.tests.load()
            self.testinfo = f"{P['good']} Found {P['bright']}{self.tests.test_count}{P['normal']} tests and {P['bright']}{self.tests.action_count}{P['normal']} actions{P['reset']}"
        except Exception as e:
            self.load_exception_happend = True
            write_exception_to_log() 
            self.testinfo = f"{Fore.RED} Test error: {Style.RESET_ALL}{e}"
            print (self.testinfo)
        try:
            self.port = self.port_finder.select_port()            
            if self.port is None:
                self.load_exception_happend = True
                self.port = f"{Fore.RED} Ports error: {Style.RESET_ALL} No suitable ports found"
        except Exception as e:
            self.load_exception_happend = True
            write_exception_to_log()
            print(f"\t{Fore.RED} Error connecting to device: {Style.RESET_ALL}{e}")
        if self.load_exception_happend:
            try:
                input(f"\n{Style.BRIGHT} Press Enter to Continue...{Style.NORMAL}")
            except:
                exit(-1)

    def main_menu(self):
        """Main menu logic and state calculation"""
        try:
            # 1. CALCULATE FACTS (The "State")
            has_op = self.operator_name not in [None, self.NOT_AVAILABLE, ""]
            has_sn = self.launcher_sn not in [None, self.NOT_AVAILABLE, ""]
            
            # Port detection logic
            is_port_valid = hasattr(self.port, 'vid') and self.port.vid in [11914, 9114]
            is_port_error = isinstance(self.port, str) # Usually means an error message string
            
            # Test loading logic
            tests_loaded = not self.tests.error and self.tests.action_count >= 1 and self.tests.test_count >= 1
            
            # "Can Run" requires a valid port AND loaded tests
            can_run_tests = tests_loaded and is_port_valid
            # "Is Recommended" requires operator and SN to be set
            is_ready_to_run = can_run_tests and has_op and has_sn

            # 2. MAP FACTS TO PROPS (The "View Model")
            props = {
                "logo": self.logo,
                "operator_name": self.operator_name,
                "launcher_sn": self.launcher_sn,
                
                # Formatting the port string
                "port_display": (f"{P['bright']}{self.port.name}{P['normal']} {self.port.description}" 
                                if is_port_valid else self.port),
                
                # Formatting test info
                "test_info_str": (f"\t\t{P['error']}{self.testinfo}{P['reset']}" 
                                if not tests_loaded else self.testinfo),

                # Mapping semantic colors
                "op_color":   P['good'] if has_op else P['warning'],
                "sn_color":   P['good'] if has_sn else P['warning'],
                "port_color": P['good'] if is_port_valid else (P['error'] if is_port_error else P['warning']),
                
                # Run button logic: Red if blocked, Yellow if missing data, Green if perfect
                "run_color":  P['good'] if is_ready_to_run else (P['warning'] if can_run_tests else P['error'])
            }

            # 3. RENDER
            # clear_terminal()  # Assuming this exists in your scope
            print(render_main_menu(props))

        except Exception:
            traceback.print_exc()

        # 4. INTERACTION
        try:
            return input(f"\n{P['bright']} Select a number and Press Enter to Continue...{P['normal']} sssssss")
        except KeyboardInterrupt:
            exit(-1)
        except Exception:
            import traceback
            traceback.print_exc()



        
if __name__ == '__main__':
    just_fix_windows_console()  # if in a windows terminal, wrap stdin stdout in
                                # a file objects that intercepts ANSI sequences
                                # and runs the appropriate commands to emulate 
                                # ANSI sequences on windows
    
    setup_logger(get_base_dir() / "debug_log.txt")
    try:
        app = App()
        app.run()
    except Exception as e:
        write_exception_to_log()
        raise e
