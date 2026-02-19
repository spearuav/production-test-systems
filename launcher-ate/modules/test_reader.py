# launcher-ate/modules/test_reader.py
from modules.util import get_base_dir


class Test_reader:
    """Reads and validates test configurations"""
    
    def __init__(self):
        self.base_dir = get_base_dir()
        self.tests_dir = self.base_dir / "tests"
        self.actions = self.base_dir / "actions"
        
    def load(self):
        """Load test information and validate required files"""
        # Check if tests directory exists
        if not self.tests_dir.exists():
            raise FileNotFoundError(f"Tests directory not found: {self.tests_dir}")
        
        # Check if actions directory exists
        if not self.actions.exists():
            raise FileNotFoundError(f"actions directory not found: {self.actions}")
        
        # Validate setup.py in actions
        setup_py = self.actions / "setup.py"
        if not setup_py.exists():
            raise FileNotFoundError(f"setup.py not found in actions directory: {setup_py}")
        
        # Validate iperf.py in tests
        iperf_py = self.tests_dir / "iperf.py"
        if not iperf_py.exists():
            raise FileNotFoundError(f"iperf.py not found in tests directory: {iperf_py}")
        
        # Count tests and actions
        test_count = 0
        action_count = 0

        # Count files in tests directory (excluding setup.py and iperf.py)
        if self.tests_dir.exists():
            for item in self.tests_dir.iterdir():
                test_count += 1

        # Count files in actions directory (excluding setup.py)
        if self.actions.exists():
            for item in self.actions.iterdir():
                action_count += 1

        # If we get here, all required files exist
        return f"Found {test_count} tests and {action_count} actions."
