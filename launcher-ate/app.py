

from colorama import Fore, Back, Style, just_fix_windows_console
from pathlib import Path
from enum import IntEnum,auto
from modules.logo_reader import Logo_reader
from modules.test_reader import Test_reader
from modules.port_finder import Port_finder
import traceback
from modules.util import  set_base_dir, get_base_dir, logger, setup_logger,\
    write_exception_to_log, clear_terminal

# Initialize BASE_DIR directly
set_base_dir(__file__)

class App():
    """Main app, orchestrates and runs stuff"""

    NO_TEST_INFO = "No tests Found"
    NOT_AVAILABLE = "NA"

    def __init__(self):
        self.logo_reader = Logo_reader(get_base_dir())
        self.logo:str = None
        self.tests = Test_reader()
        self.testinfo = self.NO_TEST_INFO
        self.port_finder = Port_finder()
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
            self.testinfo = self.tests.load()
        except Exception as e:
            self.load_exception_happend = True
            write_exception_to_log() 
            self.testinfo = f"\t{Fore.RED} Test error: {Style.RESET_ALL}{e}"
            print (self.testinfo)
        try:
            self.port = self.port_finder.select_port()            
            if self.port is None:
                self.load_exception_happend = True
                self.port = f"\t{Fore.RED} Ports error: {Style.RESET_ALL} No suitable ports found"
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
        """Main menu for the application"""
        """Display the main menu with colored options"""
        try:
            clear_terminal()
            print(self.logo)
            print("\n" + "="*50)
            print("           MAIN MENU")
            print("="*50)

            missing_user_or_sn = False
            color = Fore.GREEN
            if(self.operator_name in [None,self.NOT_AVAILABLE,""]):
                color = Fore.YELLOW
                missing_user_or_sn = True
            print(f"\t\t{color}Operator Name:{Style.RESET_ALL} {self.operator_name}")
            print(f"{color}1. Set Operator Name{Style.RESET_ALL}")



            if(self.launcher_sn in [None,self.NOT_AVAILABLE,""]):
                color = Fore.YELLOW
                missing_user_or_sn = True
            else:
                color = Fore.GREEN
            print(f"\t\t{color}Launcher SN#:{Style.RESET_ALL} {self.launcher_sn}")
            print(f"{color}2. Set Launcher SN#{Style.RESET_ALL}")

            can_run_tests=True
            if(type (self.port) is str):
                color = Fore.RED
                print(f"\t\t{color}Serial port:{Style.RESET_ALL} {self.port}")
                can_run_tests=False
            else:
                color = Fore.GREEN if self.port.vid in [11914, 9114] else Fore.YELLOW
                print(f"\t\t{color}Serial port:{Style.RESET_ALL} {Style.BRIGHT}{self.port.name}{Style.NORMAL} {self.port.description}")
            print(f"{Fore.BLUE}3. Select USB Port{Style.RESET_ALL}")

            if self.testinfo is None:
                print(f"\t\t{Fore.RED}Couldn't load tests!{Style.RESET_ALL}")
                can_run_tests=False
            else:
                print(f"{Fore.RED}{self.testinfo}{Style.RESET_ALL}")             
                can_run_tests=False
            if can_run_tests:
                if missing_user_or_sn:
                    color = Fore.YELLOW
                else:
                    color = Fore.GREEN
            else:
                color = Fore.RED
            print(f"{color}4. Run Tests{Style.RESET_ALL}")
            print(f"{color}5. Run a Single Test{Style.RESET_ALL}")
            print(f"{Fore.BLUE}6. Reload Tests{Style.RESET_ALL}")
            print(f"{Fore.BLUE}7. Exit{Style.RESET_ALL}")
            print("="*50)
        except:
            import traceback
            traceback.print_exc()
        try:
            input(f"\n{Style.BRIGHT} Select a number and Press Enter to Continue...{Style.NORMAL}")
        except KeyboardInterrupt:
            exit(-1)


        
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
