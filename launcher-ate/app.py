from ctypes import util
from encodings.punycode import T

from colorama import Fore, Back, Style, just_fix_windows_console
from pathlib import Path
from enum import IntEnum,auto
from modules.logo_reader import LogoReader
from modules.test_reader import TestReader
from modules.test_loader import TestLoader
from modules.test_runner import TestRunner
from modules.test_context import TestContext
from modules.atr_writer import ATRWriter
from modules.port_finder import PortFinder, PortInfo
from modules.util import  set_base_dir, get_base_dir, logger, setup_logger,\
    write_exception_to_log, clear_terminal, TestLogger
from menu.style import PALETTE as P
from menu.main_menu import render_main_menu
from menu.port_selector import render_port_selector, color_selector as port_color

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
        self.port_error = None
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
        self.load_exception_happend = False
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
            self.port_finder.select_port()
            inf_port = self.port_finder.inf_current_port
            if inf_port is None:
                self.load_exception_happend = True
                self.port_error = f"{Fore.RED} Ports error: {Style.RESET_ALL} No suitable ports found"
        except Exception as e:
            self.load_exception_happend = True
            write_exception_to_log()
            print(f"\t{Fore.RED} Error connecting to device: {Style.RESET_ALL}{e}")
        if self.load_exception_happend:
            try:
                input(f"\n{Style.BRIGHT} Press Enter to Continue...{Style.NORMAL}")
            except:
                exit(-1)

    def make_test_context(self):
            """Create a TestContext with logger and ATRWriter."""
            return TestContext(
                operator_name=self.operator_name,
                launcher_sn=self.launcher_sn,
                logger=TestLogger(get_base_dir() / "test_logs"),
                atr_writer=ATRWriter(get_base_dir() / "atr_log", self.tests.tests)
            )

    def main_menu(self):
        """Main menu logic and state calculation"""
        try:
            # 1. CALCULATE FACTS (The "State")

            inf_port = self.port_finder.inf_current_port
            has_op = self.operator_name not in [None, self.NOT_AVAILABLE, ""]
            has_sn = self.launcher_sn not in [None, self.NOT_AVAILABLE, ""]
            
            # Port detection logic
            is_port_valid = inf_port is not None and (inf_port.probed or inf_port.known_vid)
            is_port_error = isinstance(inf_port, str) or inf_port is None or not inf_port.is_usb # Usually means an error message string
            
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
                "port_display": f"{port_color(inf_port)} {P['bright']}{inf_port.port.name}{P['normal']} {inf_port.port.description}"
                                if isinstance(inf_port, PortInfo) else
                                f"{P['error']}{self.port_error}{P['reset']}",  # If
                
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
            input_ = input(f"\n{P['bright']} Select a number and Press Enter to Continue: {P['normal']}")
            options = {
                "1": self.operator_name_entry,
                "2": self.launcher_sn_entry,
                "3": self.select_port,
                "4": self.run_tests,
                "5": self.run_test_menu,
                "6": self.reload_data,
                "7": self.exit,
            }
            if input_ in options:
                self.state=options[input_]
        except KeyboardInterrupt as e:
            raise e
        except Exception:
            import traceback
            traceback.print_exc()

    def operator_name_entry(self):

        has_op =  self.operator_name not in [None, self.NOT_AVAILABLE, ""]
        print(f"""\
            Current SN: {P['good'] if has_op else P['warning']}{self.operator_name}
            Write a new SN or leave empty to keep current SN: """)
        try:
            input_ = input()
            if input_:
                self.operator_name = input_
        except KeyboardInterrupt:
            pass
        finally:
            self.state = self.main_menu

    def launcher_sn_entry(self):
        has_sn =  self.launcher_sn not in [None, self.NOT_AVAILABLE, ""]
        print(f"""\
            Current SN: {P['good'] if has_sn else P['warning']}{self.launcher_sn}
            Write a new SN or leave empty to keep current SN: """)
        try:
            input_ = input()
            if input_:
                self.launcher_sn = input_
        except KeyboardInterrupt:
            pass
        finally:
            self.state = self.main_menu

    def select_port(self):
        last_action = None
        while True:
            props={
                "logo": self.logo,
                "PortInfoList" : self.port_finder.get_serial_ports(),
                "current_port" : self.port_finder.inf_current_port,
                "last_action": last_action
            }
            # 3. RENDER
            clear_terminal()  # Assuming this exists in your scope
            print(render_port_selector(props))

            input_ = input(f"\n{P['bright']} Write a port number and Press Enter to Continue\n or write one of the options (p, a, s, b): {P['normal']}")
            input_ = input_.lower()

            if input_ == "b":
                self.state = self.main_menu
                return
            elif input_ == "p":
                if self.port_finder.inf_current_port is not None:
                    result = self.port_finder.probe(self.port_finder.inf_current_port)
                    last_action = f"Probed {self.port_finder.inf_current_port.port.name}: {'Success' if result == True else f'Failed ({result})'}"
                else:
                    last_action = "No port selected to probe."
            elif input_ == "a":
                candidates = self.port_finder.find_port_candidates()
                if not candidates:
                    last_action = "No candidate ports found to probe."
                else:
                    results = []
                    for port in candidates:
                        result = self.port_finder.probe(port)
                        results.append((port, result))
                    last_action = "Auto-probe results:\n" + "\n".join([f"{port.port.name}: {'Success' if res == True else f'Failed ({res})'}" for port, res in results])
            elif input_ == "s":
                self.port_finder.get_serial_ports()  # Refresh the port list
                last_action = "Port list refreshed."
            elif input_.isdigit():
                index = int(input_) - 1
                ports = self.port_finder.get_serial_ports()
                if 0 <= index < len(ports):
                    self.port_finder.inf_current_port = ports[index]
                    last_action = f"Selected port: {ports[index].port.name}"
                else:
                    last_action = "Invalid port number."
            else:
                last_action = "Invalid input. Please try again."

    def run_tests(self):
        """Run all tests and log the results."""
        try:
            context = self.make_test_context()
            test_loader = TestLoader(tests_dir=self.tests.tests_dir, actions_dir=self.tests.actions_dir)
            # Attach actions and tests attributes for compatibility
            test_loader.actions = self.tests.actions
            test_loader.tests = self.tests.tests
            runner = TestRunner(test_loader)
            runner.run_all_tests(context)
        except Exception as e:
            self.load_exception_happend = True
            write_exception_to_log()
            print(f"{Fore.RED}Error running tests: {Style.RESET_ALL}{e}")
        finally:
            self.state = self.main_menu

    def run_test_menu(self):
        """Display a menu to select and run a single test."""
        try:
            test_name = self.select_test()
            if test_name is None:
                self.state = self.main_menu
                return
            test_loader = TestLoader(tests_dir=self.tests.tests_dir, actions_dir=self.tests.actions_dir)
            # Attach actions and tests attributes for compatibility
            test_loader.actions = self.tests.actions
            test_loader.tests = self.tests.tests
            runner = TestRunner(test_loader)

            context = self.make_test_context()
            runner.run_single_test(context, test_name)
        except Exception as e:
            self.load_exception_happend = True
            write_exception_to_log()
            print(f"{Fore.RED}Error running test: {Style.RESET_ALL}{e}")

    def select_test(self):
        """Display a menu to select a test, with option to go back."""
        print(f"{Fore.CYAN}Available Tests:{Style.RESET_ALL}")
        for i, test in enumerate(self.tests.tests, start=1):
            print(f"{i}. {test}")
        print(f"b. Back")
        while True:
            choice = input(f"{Fore.YELLOW}Select a test by number or 'b' to go back: {Style.RESET_ALL}").strip().lower()
            if choice == 'b':
                return None
            try:
                num = int(choice)
                if 1 <= num <= len(self.tests.tests):
                    return self.tests.tests[num - 1]
                else:
                    print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid input. Please enter a number or 'b'.{Style.RESET_ALL}")

    def reload_data(self):
        clear_terminal()
        self.load_data()
        self.state = self.main_menu

    def exit(self):
        # TODO: add cleanup code if there is any
        exit(0)


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
