import time
from modules.test_loader import TestLoader
from modules.test_context import TestContext, TestResult

class TestRunner:
    """
    TestRunner manages test execution, logging, and timing.
    It keeps logger, ATRWriter, operator info private and only passes 
    a clean TestContext to tests.
    """
    def __init__(self, test_loader: TestLoader, logger, atr_writer, operator_name, launcher_sn):
        self.test_loader = test_loader
        self.logger = logger
        self.atr_writer = atr_writer
        self.operator_name = operator_name
        self.launcher_sn = launcher_sn
        self.context = TestContext()
        self.test_results = {}

    def _log(self, message):
        """Internal logging method."""
        if self.logger:
            self.logger.info(message)

    def _inject_context_into_module(self, module):
        """
        Inject context resources into the test module's global namespace.
        This allows tests to use resources directly without prefixes.
        
        Example: Instead of context.ON.set(True), just use ON.set(True)
        """
        # Inject all readable properties
        for attr_name in ['ON_RTRN', 'OFF_RTRN', 'BIT_STAT', 'BIT_IND', 'DRN_PRES', 
                          'CAP_PRES', 'Blue', 'Green', 'Inflator', 'Charge', 'V5_UUT']:
            setattr(module, attr_name, getattr(self.context, attr_name))
        
        # Inject all setable properties
        for attr_name in ['ON', 'OFF', 'INF_EN', 'CHRG_EN', 'TRIG', 
                          'LAUNCH_EN', 'LAUNCH_CONSENT']:
            setattr(module, attr_name, getattr(self.context, attr_name))
        
        # Inject utility methods
        setattr(module, 'fail', self.context.fail)
        setattr(module, 'success', self.context.success)
        setattr(module, 'operator_action', self.context.operator_action)
        setattr(module, 'iperf', self.context.iperf)
        
        # Inject utility functions
        setattr(module, 'test_time_to_trigger', self.context.test_time_to_trigger)
        setattr(module, 'test_time_to_value', self.context.test_time_to_value)
        setattr(module, 'test_stable', self.context.test_stable)
        
        # Inject config dicts (as references so changes persist)
        setattr(module, 'i2c', self.context.i2c)
        setattr(module, 'op_timeout', self.context.op_timeout)

    def _run_module(self, module_name, module_type="test"):
        """
        Load and execute a test or action module with context.
        Logs start, finish, time elapsed, and result.
        
        Args:
            module_name: Name of the test/action module to run
            module_type: Either "test" or "action"
        
        Returns:
            tuple: (success: bool, message: str, elapsed_time: float)
        """
        start_time = time.time()
        
        # Log start
        self._log(f"========================================")
        self._log(f"Starting {module_type}: {module_name}")
        self._log(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        self._log(f"========================================")
        
        success = False
        message = ""
        
        try:
            # Load the module
            if module_type == "action":
                module = self.test_loader.load_action(module_name)
            else:
                module = self.test_loader.load_test(module_name)
            
            # Inject context resources into module globals for clean access
            self._inject_context_into_module(module)
            
            # Execute the module's run function with context
            if hasattr(module, 'run'):
                module.run(self.context)
                success = True
                message = f"{module_type.capitalize()} completed successfully"
            else:
                success = False
                message = f"Error: {module_type} '{module_name}' does not have a 'run' function"
                
        except TestResult as tr:
            # Test explicitly called success() or fail()
            success = tr.success
            message = str(tr)
            
        except Exception as e:
            # Unexpected error
            success = False
            message = f"Error: {str(e)}"
            self._log(f"Exception details: {type(e).__name__}: {e}")
            import traceback
            self._log(traceback.format_exc())
        
        finally:
            # Calculate elapsed time
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            # Log finish
            status = "✅ PASSED" if success else "❌ FAILED"
            self._log(f"----------------------------------------")
            self._log(f"{module_type.capitalize()} {status}: {module_name}")
            self._log(f"Result: {message}")
            self._log(f"Time elapsed: {elapsed_time:.3f} seconds")
            self._log(f"========================================\n")
            
            # Unload the module to allow fresh reloads
            self.test_loader.unload_module(module_name)
            
            return success, message, elapsed_time

    def run_all_tests(self):
        """Run all tests with setup, reset between tests, and teardown."""
        self._log(f"\n{'='*60}")
        self._log(f"TEST RUN STARTED")
        self._log(f"Operator: {self.operator_name}")
        self._log(f"Launcher SN: {self.launcher_sn}")
        self._log(f"{'='*60}\n")
        
        run_start_time = time.time()
        
        # Run setup action if it exists
        if "setup" in self.test_loader.actions:
            self._run_module("setup", "action")

        # Run all tests
        for test_name in self.test_loader.tests:
            success, message, elapsed = self._run_module(test_name, "test")
            self.test_results[test_name] = success
            
            # Run reset action between tests if it exists
            if "reset" in self.test_loader.actions:
                self._run_module("reset", "action")

        # Run teardown action if it exists
        if "teardown" in self.test_loader.actions:
            self._run_module("teardown", "action")
        
        # Calculate total run time
        run_end_time = time.time()
        total_time = run_end_time - run_start_time
        
        # Summary
        passed_count = sum(1 for result in self.test_results.values() if result)
        failed_count = len(self.test_results) - passed_count
        
        self._log(f"\n{'='*60}")
        self._log(f"TEST RUN COMPLETED")
        self._log(f"Total tests: {len(self.test_results)}")
        self._log(f"Passed: {passed_count}")
        self._log(f"Failed: {failed_count}")
        self._log(f"Total time: {total_time:.3f} seconds")
        self._log(f"{'='*60}\n")
        
        # Write to ATR if available
        if self.atr_writer:
            # TODO: Implement ATR writing logic
            pass
        
        return self.test_results

    def run_single_test(self, test_name: str):
        """Run a single test with setup."""
        self._log(f"\n{'='*60}")
        self._log(f"SINGLE TEST RUN")
        self._log(f"Test: {test_name}")
        self._log(f"Operator: {self.operator_name}")
        self._log(f"Launcher SN: {self.launcher_sn}")
        self._log(f"{'='*60}\n")
        
        # Run setup action if it exists
        if "setup" in self.test_loader.actions:
            self._run_module("setup", "action")

        # Run the test
        success, message, elapsed = self._run_module(test_name, "test")
        
        self._log(f"Test {'PASSED' if success else 'FAILED'}")
        
        return success, message, elapsed
